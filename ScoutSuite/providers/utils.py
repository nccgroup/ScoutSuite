import asyncio
import inspect
import re
from hashlib import sha1

from ScoutSuite.core.console import print_info, print_warning
from ScoutSuite.providers.aws.utils import is_throttled as aws_is_throttled
from ScoutSuite.providers.gcp.utils import is_throttled as gcp_is_throttled


def get_non_provider_id(name):
    """
    Not all resources have an ID and some services allow the use of "." in names, which breaks Scout's
    recursion scheme if name is used as an ID. Use SHA1(name) instead.

    :param name:                    Name of the resource to
    :return:                        SHA1(name)
    """
    name_hash = sha1()
    name_hash.update(name.encode('utf-8'))
    return f'scoutid-{name_hash.hexdigest()}'


async def run_concurrently(function, backoff_seconds=15):
    try:
        async with asyncio.get_event_loop().throttler:
            return await run_function_concurrently(function)
    except Exception as e:
        raise
        """
        Commented out so this does not trigger errors from is_throttled, which is not fully implemented
        # Determine whether the exception is due to API throttling
        if is_throttled(e):
            source_file = inspect.getsourcefile(function)
            source_file_line = inspect.getsourcelines(function)[1]
            print_warning(f'Hitting API rate limiting ({"/".join(source_file.split("/")[-2:])} L{source_file_line}), will retry in {backoff_seconds}s')
            await asyncio.sleep(backoff_seconds)
            return await run_concurrently(function, backoff_seconds + 15)
        else:
            raise
        """


def run_function_concurrently(function):
    """
    Schedules the execution of function `function` in the default thread pool (referred as 'executor') that has been
    associated with the global event loop.

    :param function: function to be executed concurrently, in a dedicated thread.
    :return: an asyncio.Future to be awaited.
    """

    return asyncio.get_event_loop().run_in_executor(executor=None, func=function)


async def get_and_set_concurrently(get_and_set_funcs: [], entities: [], **kwargs):
    """
    Given a list of get_and_set_* functions (ex: get_and_set_description, get_and_set_attributes,
    get_and_set_policy, etc.) and a list of entities (ex: stacks, keys, load balancers, vpcs, etc.),
    get_and_set_concurrently will call each of these functions concurrently on each entity.

    :param get_and_set_funcs: list of functions that takes a region and an entity (they must have the following
    signature: region: str, entity: {}) and then fetch and set some kind of attributes to this entity.
    :param entities: list of a same kind of entities
    :param kwargs: used to pass cloud provider specific parameters (ex: region or vpc for AWS, etc.) to the given
    functions.

    :return:
    """

    if len(entities) == 0:
        return

    tasks = {
        asyncio.ensure_future(
            get_and_set_func(entity, **kwargs)
        ) for entity in entities for get_and_set_func in get_and_set_funcs
    }
    await asyncio.wait(tasks)


async def map_concurrently(coroutine, entities, **kwargs):
    """
    Given a list of entities, executes coroutine `coroutine` concurrently on each entity and returns a list of the
    obtained results ([await coroutine(entity_x), await coroutine(entity_a), ..., await coroutine(entity_z)]).

    :param coroutine: coroutine to be executed concurrently. Takes an entity as parameter and returns a new entity.
    If the given coroutine does some exception handling, it should ensure to propagate the handled exceptions so
    `map_concurrently` can handle them as well (in particular ignoring them) to avoid `None` values in the list
    returned.
    :param entities: a list of the same type of entity (ex: cluster ids)

    :return: a list of new entities (ex: clusters)
    """

    if len(entities) == 0:
        return []

    results = []

    tasks = {
        asyncio.ensure_future(
            coroutine(entity, **kwargs)
        ) for entity in entities
    }

    for task in asyncio.as_completed(tasks):
        try:
            result = await task
        except Exception:
            pass
        else:
            results.append(result)

    return results


def is_throttled(exception):
    """
    Function that tries to determine if an exception was caused by throttling
    TODO - this implementation is incomplete
    """

    if hasattr(exception, 'message') and \
            ('Google Cloud' in exception.message or
             '404' in exception.message or
             'projects/' in exception.message):
        return False
    else:
        return aws_is_throttled(exception) or gcp_is_throttled(exception)


secret_patterns = {
    "AWS key":
        re.compile("(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}"),
    "Adobe Client ID (Oauth Web)":
        re.compile("(adobe[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-f0-9]{32})['\"]"),
    "Adobe Client Secret":
        re.compile("(p8e-)(?i)[a-z0-9]{32}"),
    "Alibaba AccessKey ID":
        re.compile("(LTAI)(?i)[a-z0-9]{20}"),
    "Alibaba Secret Key":
        re.compile("(alibaba[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{30})['\"]"),
    "Asana Client ID":
        re.compile("(asana[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([0-9]{16})['\"]"),
    "Asana Client Secret":
        re.compile("(asana[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{32})['\"]"),
    "Atlassian API token":
        re.compile("(atlassian[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{24})['\"]"),
    "Beamer API token":
        re.compile("(beamer[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"](b_[a-z0-9=_\-]{44})['\"]"),
    "Bitbucket client ID":
        re.compile("(bitbucket[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{32})['\"]"),
    "Bitbucket client secret":
        re.compile("(bitbucket[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9_\-]{64})['\"]"),
    "Clojars API token":
        re.compile("(CLOJARS_)(?i)[a-z0-9]{60}"),
    "Contentful delivery API token":
        re.compile("(contentful[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9\-=_]{43})['\"]"),
    "Databricks API token":
        re.compile("dapi[a-h0-9]{32}"),
    "Discord API key":
        re.compile("(discord[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-h0-9]{64})['\"]"),
    "Discord client ID":
        re.compile("(discord[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([0-9]{18})['\"]"),
    "Discord client secret":
        re.compile("(discord[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9=_\-]{32})['\"]"),
    "Doppler API token":
        re.compile("['\"](dp\.pt\.)(?i)[a-z0-9]{43}['\"]"),
    "Dropbox API secret/key":
        re.compile("(dropbox[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{15})['\"]"),
    "Dropbox long lived API token":
        re.compile(
            "(dropbox[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"][a-z0-9]{11}(AAAAAAAAAA)[a-z0-9\-_=]{43}['\"]"),
    "Dropbox short lived API token":
        re.compile(
            "(dropbox[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"](sl\.[a-z0-9\-=_]{135})['\"]"),
    "Duffel API token":
        re.compile("['\"]duffel_(test|live)_(?i)[a-z0-9_-]{43}['\"]"),
    "Dynatrace API token":
        re.compile("['\"]dt0c01\.(?i)[a-z0-9]{24}\.[a-z0-9]{64}['\"]"),
    "EasyPost API token":
        re.compile("['\"]EZAK(?i)[a-z0-9]{54}['\"]"),
    "EasyPost test API token":
        re.compile("['\"]EZTK(?i)[a-z0-9]{54}['\"]"),
    "Fastly API token":
        re.compile("(fastly[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9\-=_]{32})['\"]"),
    "Finicity API token":
        re.compile("(finicity[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-f0-9]{32})['\"]"),
    "Finicity client secret":
        re.compile("(finicity[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{20})['\"]"),
    "Flutterwave encrypted key":
        re.compile("FLWSECK_TEST[a-h0-9]{12}"),
    "Flutterwave public key":
        re.compile("FLWPUBK_TEST-(?i)[a-h0-9]{32}-X"),
    "Flutterwave secret key":
        re.compile("FLWSECK_TEST-(?i)[a-h0-9]{32}-X"),
    "Frame.io API token":
        re.compile("fio-u-(?i)[a-z0-9\-_=]{64}"),
    "Generic API Key":
        re.compile(
            "((key|api[^Version]|token|secret|password)[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([0-9a-zA-Z\-_=]{8,64})['\"]"),
    "Generic Password":
        re.compile("password"),
    "Generic Secret":
        re.compile("secret"),
    "GitHub App Token":
        re.compile("(ghu|ghs)_[0-9a-zA-Z]{36}"),
    "GitHub OAuth Access Token":
        re.compile("gho_[0-9a-zA-Z]{36}"),
    "GitHub Personal Access Token":
        re.compile("ghp_[0-9a-zA-Z]{36}"),
    "GitHub Refresh Token":
        re.compile("ghr_[0-9a-zA-Z]{76}"),
    "GitLab Personal Access Token":
        re.compile("glpat-[0-9a-zA-Z\-\_]{20}"),
    "GoCardless API token":
        re.compile("['\"]live_(?i)[a-z0-9\-_=]{40}['\"]"),
    "Google (GCP) Service-account":
        re.compile("\"type\": \"service_account\""),
    "Grafana API token":
        re.compile("['\"]eyJrIjoi(?i)[a-z0-9\-_=]{72,92}['\"]"),
    "HashiCorp Terraform user/org API token":
        re.compile("['\"](?i)[a-z0-9]{14}\.atlasv1\.[a-z0-9\-_=]{60,70}['\"]"),
    "Heroku API Key":
        re.compile(
            "(heroku[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})['\"]"),
    "Intercom API token":
        re.compile("(intercom[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9=_]{60})['\"]"),
    "Intercom client secret/ID":
        re.compile(
            "(intercom[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-h0-9]{8}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{12})['\"]"),
    "Ionic API token":
        re.compile("(ionic[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"](ion_[a-z0-9]{42})['\"]"),
    "Linear API token":
        re.compile("lin_api_(?i)[a-z0-9]{40}"),
    "Linear client secret/ID":
        re.compile("(linear[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-f0-9]{32})['\"]"),
    "LinkedIn Client ID":
        re.compile("(linkedin[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{14})['\"]"),
    "LinkedIn Client secret":
        re.compile("(linkedin[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z]{16})['\"]"),
    "Lob API Key":
        re.compile("(lob[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]((live|test)_[a-f0-9]{35})['\"]"),
    "Lob Publishable API Key":
        re.compile(
            "(lob[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]((test|live)_pub_[a-f0-9]{31})['\"]"),
    "Mailchimp API key":
        re.compile("(mailchimp[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-f0-9]{32}-us20)['\"]"),
    "Mailgun private API token":
        re.compile("(mailgun[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"](key-[a-f0-9]{32})['\"]"),
    "Mailgun public validation key":
        re.compile("(mailgun[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"](pubkey-[a-f0-9]{32})['\"]"),
    "Mailgun webhook signing key":
        re.compile(
            "(mailgun[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-h0-9]{32}-[a-h0-9]{8}-[a-h0-9]{8})['\"]"),
    "MessageBird API token":
        re.compile("(messagebird[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{25})['\"]"),
    "New Relic ingest browser API token":
        re.compile("['\"](NRJS-[a-f0-9]{19})['\"]"),
    "New Relic user API ID":
        re.compile("(newrelic[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([A-Z0-9]{64})['\"]"),
    "New Relic user API Key":
        re.compile("['\"](NRAK-[A-Z0-9]{27})['\"]"),
    "PGP private key":
        re.compile("-----BEGIN PGP PRIVATE KEY BLOCK-----"),
    "PKCS8 private key":
        re.compile("-----BEGIN PRIVATE KEY-----"),
    "PlanetScale API token":
        re.compile("pscale_tkn_(?i)[a-z0-9\-_\.]{43}"),
    "PlanetScale password":
        re.compile("pscale_pw_(?i)[a-z0-9\-_\.]{43}"),
    "Postman API token":
        re.compile("PMAK-(?i)[a-f0-9]{24}\-[a-f0-9]{34}"),
    "Pulumi API token":
        re.compile("pul-[a-f0-9]{40}"),
    "PyPI upload token":
        re.compile("pypi-AgEIcHlwaS5vcmc[A-Za-z0-9\-_]{50,1000}"),
    "RSA private key":
        re.compile("-----BEGIN RSA PRIVATE KEY-----"),
    "Rubygem API token":
        re.compile("rubygems_[a-f0-9]{48}"),
    "SSH (DSA) private key":
        re.compile("-----BEGIN DSA PRIVATE KEY-----"),
    "SSH (EC) private key":
        re.compile("-----BEGIN EC PRIVATE KEY-----"),
    "SSH private key":
        re.compile("-----BEGIN OPENSSH PRIVATE KEY-----"),
    "SendGrid API token":
        re.compile("SG\.(?i)[a-z0-9_\-\.]{66}"),
    "Sendinblue API token":
        re.compile("xkeysib-[a-f0-9]{64}\-(?i)[a-z0-9]{16}"),
    "Shippo API token":
        re.compile("shippo_(live|test)_[a-f0-9]{40}"),
    "Shopify access token":
        re.compile("shpat_[a-fA-F0-9]{32}"),
    "Shopify custom app access token":
        re.compile("shpca_[a-fA-F0-9]{32}"),
    "Shopify private app access token":
        re.compile("shppa_[a-fA-F0-9]{32}"),
    "Shopify shared secret":
        re.compile("shpss_[a-fA-F0-9]{32}"),
    "Slack token":
        re.compile("xox[baprs]-([0-9a-zA-Z]{10,48})?"),
    "Stripe":
        re.compile("(sk|pk)_(test|live)_[0-9a-z]{10,32}"),
    "Twitch API token":
        re.compile("(twitch[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{30})['\"]"),
    "Twitter token":
        re.compile("(twitter[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([a-f0-9]{35,44})['\"]"),
    "Typeform API token":
        re.compile("(typeform[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}(tfp_[a-z0-9\-_\.=]{59})"),
    "npm access token":
        re.compile("['\"](npm_(?i)[a-z0-9]{36})['\"]")
}


def is_secret(string):
    """
    Given a string, tries to identify if it includes a secret.
    :param string: String to evaluate
    :return: None if no secret identified, otherwise the type of secret
    """
    for secret_type, secret_regex in secret_patterns.items():
        if secret_regex.search(string):
            return f"{secret_type}: {string}"
    return None
