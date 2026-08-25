import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  PlayCircle, Shield, KeyRound, Sliders, ChevronRight,
  Upload, CheckCircle, AlertCircle, FileCode, Check
} from 'lucide-react';
import { scansApi, credentialsApi } from '../api';

const providers = [
  { id: 'aws', name: 'Amazon Web Services', tag: 'AWS', color: 'border-amber-500/50 hover:border-amber-400 bg-amber-500/5' },
  { id: 'azure', name: 'Microsoft Azure', tag: 'Azure', color: 'border-blue-500/50 hover:border-blue-400 bg-blue-500/5' },
  { id: 'gcp', name: 'Google Cloud Platform', tag: 'GCP', color: 'border-emerald-500/50 hover:border-emerald-400 bg-emerald-500/5' },
  { id: 'kubernetes', name: 'Kubernetes Cluster', tag: 'K8s', color: 'border-indigo-500/50 hover:border-indigo-400 bg-indigo-500/5' },
  { id: 'aliyun', name: 'Alibaba Cloud', tag: 'Aliyun', color: 'border-orange-500/50 hover:border-orange-400 bg-orange-500/5' },
  { id: 'do', name: 'DigitalOcean', tag: 'DO', color: 'border-sky-500/50 hover:border-sky-400 bg-sky-500/5' },
  { id: 'oci', name: 'Oracle Cloud', tag: 'OCI', color: 'border-red-500/50 hover:border-red-400 bg-red-500/5' },
];

export default function NewScan() {
  const navigate = useNavigate();
  const [selectedProvider, setSelectedProvider] = useState('aws');
  const [authMode, setAuthMode] = useState('vault'); // 'vault' or 'inline'
  const [savedCredentials, setSavedCredentials] = useState([]);
  const [selectedCredId, setSelectedCredId] = useState('');
  
  // AWS Inline Auth
  const [awsAuthType, setAwsAuthType] = useState('keys'); // 'keys' or 'profile'
  const [awsAccessKey, setAwsAccessKey] = useState('');
  const [awsSecretKey, setAwsSecretKey] = useState('');
  const [awsSessionToken, setAwsSessionToken] = useState('');
  const [awsProfile, setAwsProfile] = useState('');

  // Azure Inline Auth
  const [azureAuthType, setAzureAuthType] = useState('service_principal'); // 'service_principal', 'cli', 'user_account', 'user_account_browser', 'file_auth', 'msi'
  const [azureTenantId, setAzureTenantId] = useState('');
  const [azureClientId, setAzureClientId] = useState('');
  const [azureClientSecret, setAzureClientSecret] = useState('');
  const [azureUsername, setAzureUsername] = useState('');
  const [azurePassword, setAzurePassword] = useState('');
  const [azureSubscriptionId, setAzureSubscriptionId] = useState('');
  const [azureAllSubscriptions, setAzureAllSubscriptions] = useState(false);
  const [azureAuthFileContent, setAzureAuthFileContent] = useState('');

  // GCP Inline Auth
  const [gcpAuthType, setGcpAuthType] = useState('service_account'); // 'service_account' or 'user_account'
  const [gcpProjectId, setGcpProjectId] = useState('');
  const [gcpFolderId, setGcpFolderId] = useState('');
  const [gcpOrgId, setGcpOrgId] = useState('');
  const [gcpAllProjects, setGcpAllProjects] = useState(false);
  const [gcpSaJson, setGcpSaJson] = useState('');

  // Kubernetes Inline Auth
  const [k8sAuthType, setK8sAuthType] = useState('config_file'); // 'config_file' or 'default'
  const [k8sConfigContent, setK8sConfigContent] = useState('');
  const [k8sContext, setK8sContext] = useState('');
  const [k8sClusterProvider, setK8sClusterProvider] = useState('');
  const [k8sSubscriptionId, setK8sSubscriptionId] = useState('');

  // Aliyun Inline Auth
  const [aliyunAccessKeyId, setAliyunAccessKeyId] = useState('');
  const [aliyunAccessKeySecret, setAliyunAccessKeySecret] = useState('');

  // DigitalOcean Inline Auth
  const [doAuthType, setDoAuthType] = useState('token'); // 'token', 'spaces', 'both'
  const [doToken, setDoToken] = useState('');
  const [doAccessKey, setDoAccessKey] = useState('');
  const [doAccessSecret, setDoAccessSecret] = useState('');

  // OCI Inline Auth
  const [ociAuthType, setOciAuthType] = useState('direct'); // 'direct', 'config_file', 'profile'
  const [ociUserOcid, setOciUserOcid] = useState('');
  const [ociTenancyOcid, setOciTenancyOcid] = useState('');
  const [ociFingerprint, setOciFingerprint] = useState('');
  const [ociRegion, setOciRegion] = useState('us-ashburn-1');
  const [ociPrivateKey, setOciPrivateKey] = useState('');
  const [ociConfigFileContent, setOciConfigFileContent] = useState('');
  const [ociProfile, setOciProfile] = useState('DEFAULT');

  // Scan Options
  const [services, setServices] = useState('');
  const [regions, setRegions] = useState('');
  const [maxWorkers, setMaxWorkers] = useState(10);
  const [ruleset, setRuleset] = useState('default.json');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadSavedCredentials(selectedProvider);
  }, [selectedProvider]);

  const loadSavedCredentials = async (provider) => {
    try {
      const list = await credentialsApi.list(provider);
      setSavedCredentials(list);
      if (list.length > 0) {
        setSelectedCredId(list[0].id);
      } else {
        setSelectedCredId('');
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleFileUpload = (e, setter) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      setter(event.target.result);
    };
    reader.readAsText(file);
  };

  const handleStartScan = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let inlineCredentials = null;
      let effectiveAuthType = null;

      if (authMode === 'inline') {
        if (selectedProvider === 'aws') {
          effectiveAuthType = awsAuthType;
          if (awsAuthType === 'keys') {
            inlineCredentials = {
              aws_access_key_id: awsAccessKey,
              aws_secret_access_key: awsSecretKey,
              aws_session_token: awsSessionToken || undefined,
            };
          } else {
            inlineCredentials = { profile: awsProfile || 'default' };
          }
        } else if (selectedProvider === 'azure') {
          effectiveAuthType = azureAuthType;
          inlineCredentials = {
            tenant_id: azureTenantId || undefined,
            client_id: azureClientId || undefined,
            client_secret: azureClientSecret || undefined,
            username: azureUsername || undefined,
            password: azurePassword || undefined,
            subscription_ids: azureSubscriptionId ? azureSubscriptionId.split(',').map(s => s.trim()).filter(Boolean) : undefined,
            all_subscriptions: azureAllSubscriptions || undefined,
            raw_file_content: azureAuthFileContent || undefined,
          };
        } else if (selectedProvider === 'gcp') {
          effectiveAuthType = gcpAuthType;
          inlineCredentials = {
            project_id: gcpProjectId || undefined,
            folder_id: gcpFolderId || undefined,
            organization_id: gcpOrgId || undefined,
            all_projects: gcpAllProjects || undefined,
            service_account_content: gcpSaJson || undefined,
          };
        } else if (selectedProvider === 'kubernetes') {
          effectiveAuthType = k8sAuthType;
          inlineCredentials = {
            kubernetes_config_content: k8sConfigContent || undefined,
            kubernetes_context: k8sContext || undefined,
            kubernetes_cluster_provider: k8sClusterProvider || undefined,
            kubernetes_azure_subscription_id: k8sSubscriptionId || undefined,
          };
        } else if (selectedProvider === 'aliyun') {
          effectiveAuthType = 'keys';
          inlineCredentials = {
            access_key_id: aliyunAccessKeyId,
            access_key_secret: aliyunAccessKeySecret,
          };
        } else if (selectedProvider === 'do') {
          effectiveAuthType = doAuthType;
          inlineCredentials = {
            token: doToken || undefined,
            access_key: doAccessKey || undefined,
            access_secret: doAccessSecret || undefined,
          };
        } else if (selectedProvider === 'oci') {
          effectiveAuthType = ociAuthType;
          inlineCredentials = {
            auth_type: ociAuthType,
            profile: ociProfile || 'DEFAULT',
            user: ociUserOcid || undefined,
            tenancy: ociTenancyOcid || undefined,
            fingerprint: ociFingerprint || undefined,
            region: ociRegion || 'us-ashburn-1',
            private_key_content: ociPrivateKey || undefined,
            raw_file_content: ociConfigFileContent || undefined,
          };
        }

        if (inlineCredentials) {
          inlineCredentials.auth_type = effectiveAuthType;
        }
      }

      const payload = {
        provider: selectedProvider,
        auth_type: effectiveAuthType,
        credential_id: authMode === 'vault' && selectedCredId ? selectedCredId : null,
        inline_credentials: inlineCredentials,
        options: {
          services: services ? services.split(',').map(s => s.trim()).filter(Boolean) : undefined,
          regions: regions ? regions.split(',').map(r => r.trim()).filter(Boolean) : undefined,
          max_workers: parseInt(maxWorkers) || 10,
          ruleset: ruleset || 'default.json',
        }
      };

      const res = await scansApi.start(payload);
      navigate(`/scans/${res.scan_id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start scan.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">Configure New Cloud Audit</h2>
        <p className="text-sm text-slate-400 mt-1">
          Select target cloud provider, configure authentication credentials, and adjust audit scopes.
        </p>
      </div>

      {error && (
        <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl flex items-center gap-3 text-sm text-red-400">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleStartScan} className="space-y-8">
        {/* Step 1: Provider Selection */}
        <div className="bg-dark-card border border-dark-border p-6 rounded-2xl space-y-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-white">
            <span className="w-6 h-6 rounded-full bg-brand-500/20 text-brand-500 flex items-center justify-center text-xs font-bold">1</span>
            <span>Target Cloud Infrastructure</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {providers.map((p) => (
              <button
                type="button"
                key={p.id}
                onClick={() => setSelectedProvider(p.id)}
                className={`p-4 rounded-xl border text-left transition flex flex-col justify-between cursor-pointer ${
                  selectedProvider === p.id
                    ? 'border-brand-500 bg-brand-500/10 shadow-lg shadow-brand-500/10 ring-1 ring-brand-500'
                    : 'border-dark-border bg-dark-bg/60 hover:border-slate-600'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono font-bold uppercase tracking-wider text-brand-400 bg-brand-500/10 px-2 py-0.5 rounded">
                    {p.tag}
                  </span>
                  {selectedProvider === p.id && <Check className="w-4 h-4 text-brand-500" />}
                </div>
                <div className="text-xs font-medium text-slate-200">{p.name}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Step 2: Authentication Mode & Credentials */}
        <div className="bg-dark-card border border-dark-border p-6 rounded-2xl space-y-5">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-2 text-sm font-semibold text-white">
              <span className="w-6 h-6 rounded-full bg-brand-500/20 text-brand-500 flex items-center justify-center text-xs font-bold">2</span>
              <span>Authentication & Credentials ({selectedProvider.toUpperCase()})</span>
            </div>

            <div className="flex bg-dark-bg p-1 rounded-xl border border-dark-border text-xs">
              <button
                type="button"
                onClick={() => setAuthMode('vault')}
                className={`px-3 py-1.5 rounded-lg transition font-medium cursor-pointer ${
                  authMode === 'vault' ? 'bg-brand-500 text-slate-950 shadow' : 'text-slate-400 hover:text-white'
                }`}
              >
                Saved Vault Profile
              </button>
              <button
                type="button"
                onClick={() => setAuthMode('inline')}
                className={`px-3 py-1.5 rounded-lg transition font-medium cursor-pointer ${
                  authMode === 'inline' ? 'bg-brand-500 text-slate-950 shadow' : 'text-slate-400 hover:text-white'
                }`}
              >
                Direct / One-time Input
              </button>
            </div>
          </div>

          {authMode === 'vault' ? (
            <div className="space-y-3">
              {savedCredentials.length === 0 ? (
                <div className="p-6 bg-dark-bg/60 border border-dark-border border-dashed rounded-xl text-center space-y-2">
                  <KeyRound className="w-8 h-8 text-slate-500 mx-auto" />
                  <p className="text-sm text-slate-300">No stored profiles found for {selectedProvider.toUpperCase()}.</p>
                  <p className="text-xs text-slate-500">
                    Switch to "Direct / One-time Input" above or add a profile in the Credentials vault.
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {savedCredentials.map((c) => (
                    <label
                      key={c.id}
                      className={`p-4 rounded-xl border cursor-pointer flex items-center justify-between transition ${
                        selectedCredId === c.id
                          ? 'border-brand-500 bg-brand-500/10'
                          : 'border-dark-border bg-dark-bg/40 hover:border-slate-600'
                      }`}
                    >
                      <div>
                        <div className="text-sm font-semibold text-white">{c.name}</div>
                        <div className="text-xs text-slate-400 font-mono mt-0.5">Method: {c.auth_type}</div>
                      </div>
                      <input
                        type="radio"
                        name="vault_credential"
                        checked={selectedCredId === c.id}
                        onChange={() => setSelectedCredId(c.id)}
                        className="accent-brand-500 w-4 h-4"
                      />
                    </label>
                  ))}
                </div>
              )}
            </div>
          ) : (
            /* Inline Credential Inputs dynamically configured per provider */
            <div className="space-y-5 pt-2">
              {/* AWS Form */}
              {selectedProvider === 'aws' && (
                <div className="space-y-4">
                  <div className="flex gap-4">
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="aws_auth"
                        checked={awsAuthType === 'keys'}
                        onChange={() => setAwsAuthType('keys')}
                        className="accent-brand-500"
                      />
                      Access Keys (Key ID & Secret)
                    </label>
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="aws_auth"
                        checked={awsAuthType === 'profile'}
                        onChange={() => setAwsAuthType('profile')}
                        className="accent-brand-500"
                      />
                      AWS Named Profile (~/.aws/credentials)
                    </label>
                  </div>

                  {awsAuthType === 'keys' ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-xs text-slate-400 mb-1">AWS Access Key ID *</label>
                        <input
                          type="text"
                          required
                          value={awsAccessKey}
                          onChange={(e) => setAwsAccessKey(e.target.value)}
                          placeholder="AKIAIOSFODNN7EXAMPLE"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-slate-400 mb-1">AWS Secret Access Key *</label>
                        <input
                          type="password"
                          required
                          value={awsSecretKey}
                          onChange={(e) => setAwsSecretKey(e.target.value)}
                          placeholder="Secret Key"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div className="sm:col-span-2">
                        <label className="block text-xs text-slate-400 mb-1">AWS Session Token (Optional)</label>
                        <input
                          type="text"
                          value={awsSessionToken}
                          onChange={(e) => setAwsSessionToken(e.target.value)}
                          placeholder="AQoDYXdzEJr..."
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                    </div>
                  ) : (
                    <div>
                      <label className="block text-xs text-slate-400 mb-1">Named Profile Name *</label>
                      <input
                        type="text"
                        required
                        value={awsProfile}
                        onChange={(e) => setAwsProfile(e.target.value)}
                        placeholder="default"
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                    </div>
                  )}
                </div>
              )}

              {/* Azure Form */}
              {selectedProvider === 'azure' && (
                <div className="space-y-4">
                  {/* Azure Auth Method Radio Group */}
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-2">Azure Authentication Method</label>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
                      {[
                        { id: 'service_principal', label: 'Service Principal' },
                        { id: 'cli', label: 'Azure CLI (az cli)' },
                        { id: 'user_account', label: 'User Account' },
                        { id: 'user_account_browser', label: 'Browser Login (MFA)' },
                        { id: 'file_auth', label: 'SDK Auth File' },
                        { id: 'msi', label: 'Managed Identity (MSI)' },
                      ].map((m) => (
                        <label
                          key={m.id}
                          className={`p-3 rounded-xl border cursor-pointer text-xs flex items-center justify-between transition ${
                            azureAuthType === m.id
                              ? 'border-brand-500 bg-brand-500/10 text-white font-semibold'
                              : 'border-dark-border bg-dark-bg/60 text-slate-400 hover:text-white'
                          }`}
                        >
                          <span>{m.label}</span>
                          <input
                            type="radio"
                            name="azure_auth_type"
                            checked={azureAuthType === m.id}
                            onChange={() => setAzureAuthType(m.id)}
                            className="accent-brand-500"
                          />
                        </label>
                      ))}
                    </div>
                  </div>

                  {azureAuthType === 'service_principal' && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
                      <div>
                        <label className="block text-xs text-slate-400 mb-1">Tenant ID (Directory ID) *</label>
                        <input
                          type="text"
                          required
                          value={azureTenantId}
                          onChange={(e) => setAzureTenantId(e.target.value)}
                          placeholder="00000000-0000-0000-0000-000000000000"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-slate-400 mb-1">Client ID (Application ID) *</label>
                        <input
                          type="text"
                          required
                          value={azureClientId}
                          onChange={(e) => setAzureClientId(e.target.value)}
                          placeholder="00000000-0000-0000-0000-000000000000"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div className="sm:col-span-2">
                        <label className="block text-xs text-slate-400 mb-1">Client Secret *</label>
                        <input
                          type="password"
                          required
                          value={azureClientSecret}
                          onChange={(e) => setAzureClientSecret(e.target.value)}
                          placeholder="Secret value"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                    </div>
                  )}

                  {azureAuthType === 'user_account' && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
                      <div className="sm:col-span-2">
                        <label className="block text-xs text-slate-400 mb-1">Tenant ID (Directory ID) *</label>
                        <input
                          type="text"
                          required
                          value={azureTenantId}
                          onChange={(e) => setAzureTenantId(e.target.value)}
                          placeholder="00000000-0000-0000-0000-000000000000"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-slate-400 mb-1">Azure Username / Email *</label>
                        <input
                          type="text"
                          required
                          value={azureUsername}
                          onChange={(e) => setAzureUsername(e.target.value)}
                          placeholder="admin@contoso.onmicrosoft.com"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-slate-400 mb-1">Azure Password *</label>
                        <input
                          type="password"
                          required
                          value={azurePassword}
                          onChange={(e) => setAzurePassword(e.target.value)}
                          placeholder="Account password"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                    </div>
                  )}

                  {azureAuthType === 'user_account_browser' && (
                    <div className="pt-1">
                      <label className="block text-xs text-slate-400 mb-1">Tenant ID (Directory ID) *</label>
                      <input
                        type="text"
                        required
                        value={azureTenantId}
                        onChange={(e) => setAzureTenantId(e.target.value)}
                        placeholder="00000000-0000-0000-0000-000000000000"
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                    </div>
                  )}

                  {azureAuthType === 'file_auth' && (
                    <div className="space-y-2 pt-1">
                      <label className="block text-xs text-slate-400 mb-1">Upload SDK Auth JSON File *</label>
                      <input
                        type="file"
                        accept=".json"
                        required
                        onChange={(e) => handleFileUpload(e, setAzureAuthFileContent)}
                        className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-500/10 file:text-brand-400 hover:file:bg-brand-500/20"
                      />
                    </div>
                  )}

                  {azureAuthType === 'cli' && (
                    <p className="text-xs text-slate-400 bg-dark-bg/60 p-3 rounded-xl border border-dark-border">
                      Uses active Azure CLI credentials (<code className="text-brand-400">az login</code>) from the server environment.
                    </p>
                  )}

                  {azureAuthType === 'msi' && (
                    <p className="text-xs text-slate-400 bg-dark-bg/60 p-3 rounded-xl border border-dark-border">
                      Uses Managed Service Identity (MSI) inside Azure VM/Container.
                    </p>
                  )}

                  {/* Scope: Subscriptions */}
                  <div className="pt-2 border-t border-dark-border/60">
                    <label className="block text-xs text-slate-400 mb-1">Target Subscription ID(s) (Optional, comma-separated)</label>
                    <input
                      type="text"
                      disabled={azureAllSubscriptions}
                      value={azureSubscriptionId}
                      onChange={(e) => setAzureSubscriptionId(e.target.value)}
                      placeholder="e.g. sub-1, sub-2 (leave blank for default)"
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none disabled:opacity-50"
                    />
                    <label className="flex items-center gap-2 mt-2 text-xs text-slate-400 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={azureAllSubscriptions}
                        onChange={(e) => setAzureAllSubscriptions(e.target.checked)}
                        className="accent-brand-500"
                      />
                      <span>Scan All Accessible Azure Subscriptions</span>
                    </label>
                  </div>
                </div>
              )}

              {/* GCP Form */}
              {selectedProvider === 'gcp' && (
                <div className="space-y-4">
                  <div className="flex gap-4">
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="gcp_auth"
                        checked={gcpAuthType === 'service_account'}
                        onChange={() => setGcpAuthType('service_account')}
                        className="accent-brand-500"
                      />
                      Service Account Key JSON
                    </label>
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="gcp_auth"
                        checked={gcpAuthType === 'user_account'}
                        onChange={() => setGcpAuthType('user_account')}
                        className="accent-brand-500"
                      />
                      User Account (gcloud credentials)
                    </label>
                  </div>

                  {gcpAuthType === 'service_account' && (
                    <div className="space-y-2">
                      <label className="block text-xs text-slate-400 mb-1">Service Account Key JSON File *</label>
                      <input
                        type="file"
                        accept=".json"
                        required
                        onChange={(e) => handleFileUpload(e, setGcpSaJson)}
                        className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-500/10 file:text-brand-400 hover:file:bg-brand-500/20"
                      />
                    </div>
                  )}

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs text-slate-400 mb-1">GCP Project ID (Optional)</label>
                      <input
                        type="text"
                        value={gcpProjectId}
                        onChange={(e) => setGcpProjectId(e.target.value)}
                        placeholder="my-gcp-project-123"
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-slate-400 mb-1">Folder ID (Optional)</label>
                      <input
                        type="text"
                        value={gcpFolderId}
                        onChange={(e) => setGcpFolderId(e.target.value)}
                        placeholder="123456789012"
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                    </div>
                  </div>
                  <label className="flex items-center gap-2 text-xs text-slate-400 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={gcpAllProjects}
                      onChange={(e) => setGcpAllProjects(e.target.checked)}
                      className="accent-brand-500"
                    />
                    <span>Scan All Accessible GCP Projects</span>
                  </label>
                </div>
              )}

              {/* Kubernetes Form */}
              {selectedProvider === 'kubernetes' && (
                <div className="space-y-4">
                  <div className="flex gap-4">
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="k8s_auth"
                        checked={k8sAuthType === 'config_file'}
                        onChange={() => setK8sAuthType('config_file')}
                        className="accent-brand-500"
                      />
                      Kubeconfig File Upload
                    </label>
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="k8s_auth"
                        checked={k8sAuthType === 'default'}
                        onChange={() => setK8sAuthType('default')}
                        className="accent-brand-500"
                      />
                      Default Environment Kubeconfig
                    </label>
                  </div>

                  {k8sAuthType === 'config_file' && (
                    <div>
                      <label className="block text-xs text-slate-400 mb-1">Upload Kubeconfig File *</label>
                      <input
                        type="file"
                        required
                        onChange={(e) => handleFileUpload(e, setK8sConfigContent)}
                        className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-500/10 file:text-brand-400 hover:file:bg-brand-500/20"
                      />
                    </div>
                  )}

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs text-slate-400 mb-1">Cluster Provider (Optional)</label>
                      <select
                        value={k8sClusterProvider}
                        onChange={(e) => setK8sClusterProvider(e.target.value)}
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      >
                        <option value="">Generic / Standard K8s</option>
                        <option value="aks">Azure Kubernetes Service (AKS)</option>
                        <option value="eks">Amazon Elastic Kubernetes Service (EKS)</option>
                        <option value="gke">Google Kubernetes Engine (GKE)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs text-slate-400 mb-1">Context Name (Optional)</label>
                      <input
                        type="text"
                        value={k8sContext}
                        onChange={(e) => setK8sContext(e.target.value)}
                        placeholder="cluster-admin"
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                    </div>
                  </div>

                  {k8sClusterProvider === 'aks' && (
                    <div>
                      <label className="block text-xs text-slate-400 mb-1">Azure Subscription ID (for AKS)</label>
                      <input
                        type="text"
                        value={k8sSubscriptionId}
                        onChange={(e) => setK8sSubscriptionId(e.target.value)}
                        placeholder="00000000-0000-0000-0000-000000000000"
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                    </div>
                  )}
                </div>
              )}

              {/* Aliyun Form */}
              {selectedProvider === 'aliyun' && (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs text-slate-400 mb-1">Aliyun Access Key ID *</label>
                    <input
                      type="text"
                      required
                      value={aliyunAccessKeyId}
                      onChange={(e) => setAliyunAccessKeyId(e.target.value)}
                      placeholder="LTAI..."
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-slate-400 mb-1">Aliyun Access Key Secret *</label>
                    <input
                      type="password"
                      required
                      value={aliyunAccessKeySecret}
                      onChange={(e) => setAliyunAccessKeySecret(e.target.value)}
                      placeholder="Secret Key"
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    />
                  </div>
                </div>
              )}

              {/* DigitalOcean Form */}
              {selectedProvider === 'do' && (
                <div className="space-y-4">
                  <div className="flex gap-4">
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="do_auth"
                        checked={doAuthType === 'token'}
                        onChange={() => setDoAuthType('token')}
                        className="accent-brand-500"
                      />
                      Personal Access Token
                    </label>
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="do_auth"
                        checked={doAuthType === 'spaces'}
                        onChange={() => setDoAuthType('spaces')}
                        className="accent-brand-500"
                      />
                      Spaces Keys Only
                    </label>
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="do_auth"
                        checked={doAuthType === 'both'}
                        onChange={() => setDoAuthType('both')}
                        className="accent-brand-500"
                      />
                      Token + Spaces
                    </label>
                  </div>

                  {(doAuthType === 'token' || doAuthType === 'both') && (
                    <div>
                      <label className="block text-xs text-slate-400 mb-1">Personal Access Token *</label>
                      <input
                        type="password"
                        required={doAuthType === 'token'}
                        value={doToken}
                        onChange={(e) => setDoToken(e.target.value)}
                        placeholder="dop_v1_..."
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                    </div>
                  )}

                  {(doAuthType === 'spaces' || doAuthType === 'both') && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-xs text-slate-400 mb-1">Spaces Access Key *</label>
                        <input
                          type="text"
                          required={doAuthType === 'spaces'}
                          value={doAccessKey}
                          onChange={(e) => setDoAccessKey(e.target.value)}
                          placeholder="DO Spaces Access Key"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-slate-400 mb-1">Spaces Secret Key *</label>
                        <input
                          type="password"
                          required={doAuthType === 'spaces'}
                          value={doAccessSecret}
                          onChange={(e) => setDoAccessSecret(e.target.value)}
                          placeholder="DO Spaces Secret Key"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* OCI Form */}
              {selectedProvider === 'oci' && (
                <div className="space-y-4">
                  <div className="flex flex-wrap gap-4">
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="oci_auth"
                        checked={ociAuthType === 'direct'}
                        onChange={() => setOciAuthType('direct')}
                        className="accent-brand-500"
                      />
                      Direct OCIDs & API Key
                    </label>
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="oci_auth"
                        checked={ociAuthType === 'config_file'}
                        onChange={() => setOciAuthType('config_file')}
                        className="accent-brand-500"
                      />
                      Upload OCI Config (~/.oci/config)
                    </label>
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="radio"
                        name="oci_auth"
                        checked={ociAuthType === 'profile'}
                        onChange={() => setOciAuthType('profile')}
                        className="accent-brand-500"
                      />
                      Local WSL Profile
                    </label>
                  </div>

                  {ociAuthType === 'direct' && (
                    <div className="space-y-4 pt-1">
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-xs text-slate-400 mb-1">User OCID *</label>
                          <input
                            type="text"
                            required
                            value={ociUserOcid}
                            onChange={(e) => setOciUserOcid(e.target.value)}
                            placeholder="ocid1.user.oc1..aaaa..."
                            className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-slate-400 mb-1">Tenancy OCID *</label>
                          <input
                            type="text"
                            required
                            value={ociTenancyOcid}
                            onChange={(e) => setOciTenancyOcid(e.target.value)}
                            placeholder="ocid1.tenancy.oc1..aaaa..."
                            className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-slate-400 mb-1">API Key Fingerprint *</label>
                          <input
                            type="text"
                            required
                            value={ociFingerprint}
                            onChange={(e) => setOciFingerprint(e.target.value)}
                            placeholder="20:3b:97:13:55:1c:..."
                            className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none font-mono text-xs"
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-slate-400 mb-1">OCI Region *</label>
                          <input
                            type="text"
                            required
                            value={ociRegion}
                            onChange={(e) => setOciRegion(e.target.value)}
                            placeholder="us-ashburn-1"
                            className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                          />
                        </div>
                      </div>

                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <label className="block text-xs text-slate-400">OCI API Private Key (PEM format) *</label>
                          <label className="text-xs text-brand-400 hover:text-brand-300 cursor-pointer flex items-center gap-1">
                            <Upload className="w-3.5 h-3.5" />
                            <span>Upload .pem file</span>
                            <input
                              type="file"
                              accept=".pem,.key,.txt"
                              onChange={(e) => handleFileUpload(e, setOciPrivateKey)}
                              className="hidden"
                            />
                          </label>
                        </div>
                        <textarea
                          rows={4}
                          required
                          value={ociPrivateKey}
                          onChange={(e) => setOciPrivateKey(e.target.value)}
                          placeholder="-----BEGIN RSA PRIVATE KEY-----&#10;...&#10;-----END RSA PRIVATE KEY-----"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl p-3 text-xs text-slate-200 font-mono focus:border-brand-500 focus:outline-none leading-relaxed"
                        />
                      </div>
                    </div>
                  )}

                  {ociAuthType === 'config_file' && (
                    <div className="space-y-4 pt-1">
                      <div>
                        <label className="block text-xs text-slate-400 mb-1">Upload OCI Config File (~/.oci/config) *</label>
                        <input
                          type="file"
                          required
                          onChange={(e) => handleFileUpload(e, setOciConfigFileContent)}
                          className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-500/10 file:text-brand-400 hover:file:bg-brand-500/20"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-slate-400 mb-1">Upload OCI API Private Key (.pem) (If referenced in config)</label>
                        <input
                          type="file"
                          accept=".pem,.key,.txt"
                          onChange={(e) => handleFileUpload(e, setOciPrivateKey)}
                          className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-500/10 file:text-brand-400 hover:file:bg-brand-500/20"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-slate-400 mb-1">Profile Name in Config (Optional)</label>
                        <input
                          type="text"
                          value={ociProfile}
                          onChange={(e) => setOciProfile(e.target.value)}
                          placeholder="DEFAULT"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                    </div>
                  )}

                  {ociAuthType === 'profile' && (
                    <div className="pt-1">
                      <label className="block text-xs text-slate-400 mb-1">Profile Name in WSL ~/.oci/config *</label>
                      <input
                        type="text"
                        required
                        value={ociProfile}
                        onChange={(e) => setOciProfile(e.target.value)}
                        placeholder="DEFAULT"
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                      <p className="text-xs text-slate-500 mt-2">
                        Reads existing authentication profile from <code className="text-slate-400 font-mono">~/.oci/config</code> inside WSL.
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Step 3: Scan Options */}
        <div className="bg-dark-card border border-dark-border p-6 rounded-2xl space-y-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-white">
            <span className="w-6 h-6 rounded-full bg-brand-500/20 text-brand-500 flex items-center justify-center text-xs font-bold">3</span>
            <span>Audit Scope & Rulesets</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-slate-400 mb-1">Services Filter (Comma-separated, leave blank for all)</label>
              <input
                type="text"
                value={services}
                onChange={(e) => setServices(e.target.value)}
                placeholder="e.g. iam, s3, ec2, rds, cloudtrail"
                className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">Regions Filter (Comma-separated)</label>
              <input
                type="text"
                value={regions}
                onChange={(e) => setRegions(e.target.value)}
                placeholder="e.g. us-east-1, us-west-2"
                className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">Ruleset</label>
              <input
                type="text"
                value={ruleset}
                onChange={(e) => setRuleset(e.target.value)}
                placeholder="default.json"
                className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none font-mono text-xs"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">Parallel Max Workers</label>
              <input
                type="number"
                min="1"
                max="50"
                value={maxWorkers}
                onChange={(e) => setMaxWorkers(e.target.value)}
                className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
              />
            </div>
          </div>
        </div>

        {/* Submit */}
        <div className="flex justify-end gap-4">
          <button
            type="submit"
            disabled={loading}
            className="bg-brand-500 hover:bg-brand-600 disabled:opacity-50 text-slate-950 font-semibold px-6 py-3 rounded-xl flex items-center gap-2 shadow-lg shadow-brand-500/25 transition cursor-pointer"
          >
            {loading ? (
              <span className="inline-block w-5 h-5 border-2 border-slate-900 border-t-transparent rounded-full animate-spin"></span>
            ) : (
              <>
                <PlayCircle className="w-5 h-5" />
                <span>Start Security Audit</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
