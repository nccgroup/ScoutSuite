import React, { useState, useEffect } from 'react';
import { 
  KeyRound, Plus, Trash2, Shield, 
  Upload, Check, AlertCircle, FileText, Lock, Filter
} from 'lucide-react';
import { credentialsApi } from '../api';

const PROVIDER_AUTH_MODES = {
  aws: [
    { id: 'keys', label: 'Access Keys (Key ID & Secret)' },
    { id: 'profile', label: 'Named Profile (~/.aws/credentials)' },
  ],
  azure: [
    { id: 'service_principal', label: 'Service Principal (App ID, Secret & Tenant)' },
    { id: 'cli', label: 'Azure CLI (az cli active session)' },
    { id: 'user_account', label: 'User Account (Username & Password)' },
    { id: 'user_account_browser', label: 'Browser Login (Interactive MFA)' },
    { id: 'file_auth', label: 'SDK Auth JSON File' },
    { id: 'msi', label: 'Managed Service Identity (MSI)' },
  ],
  gcp: [
    { id: 'service_account', label: 'Service Account (JSON Key File)' },
    { id: 'user_account', label: 'User Account (gcloud credentials)' },
  ],
  kubernetes: [
    { id: 'config_file', label: 'Kubeconfig File Upload' },
    { id: 'default', label: 'Default System Kubeconfig (~/.kube/config)' },
  ],
  aliyun: [
    { id: 'keys', label: 'Access Keys (Key ID & Secret)' },
  ],
  do: [
    { id: 'token', label: 'Personal Access Token' },
    { id: 'spaces', label: 'Spaces Access Keys' },
    { id: 'both', label: 'API Token + Spaces Keys' },
  ],
  oci: [
    { id: 'direct', label: 'Direct OCIDs & API Key (User, Tenancy, Fingerprint, PEM)' },
    { id: 'config_file', label: 'Upload OCI Config (~/.oci/config)' },
    { id: 'profile', label: 'Named Profile (~/.oci/config)' },
  ],
};

export default function Credentials() {
  const [credentials, setCredentials] = useState([]);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Form states
  const [name, setName] = useState('');
  const [provider, setProvider] = useState('aws');
  const [authType, setAuthType] = useState('keys');
  
  // AWS Fields
  const [awsAccessKey, setAwsAccessKey] = useState('');
  const [awsSecretKey, setAwsSecretKey] = useState('');
  const [awsSessionToken, setAwsSessionToken] = useState('');
  const [awsProfile, setAwsProfile] = useState('');

  // Azure Fields
  const [azureTenantId, setAzureTenantId] = useState('');
  const [azureClientId, setAzureClientId] = useState('');
  const [azureClientSecret, setAzureClientSecret] = useState('');
  const [azureUsername, setAzureUsername] = useState('');
  const [azurePassword, setAzurePassword] = useState('');
  const [azureSubscriptions, setAzureSubscriptions] = useState('');
  const [azureAllSubscriptions, setAzureAllSubscriptions] = useState(false);

  // GCP Fields
  const [gcpProjectId, setGcpProjectId] = useState('');
  const [gcpFolderId, setGcpFolderId] = useState('');
  const [gcpOrgId, setGcpOrgId] = useState('');
  const [gcpAllProjects, setGcpAllProjects] = useState(false);

  // Kubernetes Fields
  const [k8sContext, setK8sContext] = useState('');
  const [k8sClusterProvider, setK8sClusterProvider] = useState('');
  const [k8sSubscriptionId, setK8sSubscriptionId] = useState('');

  // Aliyun Fields
  const [aliyunAccessKeyId, setAliyunAccessKeyId] = useState('');
  const [aliyunAccessKeySecret, setAliyunAccessKeySecret] = useState('');

  // DigitalOcean Fields
  const [doToken, setDoToken] = useState('');
  const [doAccessKey, setDoAccessKey] = useState('');
  const [doAccessSecret, setDoAccessSecret] = useState('');

  // OCI Fields
  const [ociUserOcid, setOciUserOcid] = useState('');
  const [ociTenancyOcid, setOciTenancyOcid] = useState('');
  const [ociFingerprint, setOciFingerprint] = useState('');
  const [ociRegion, setOciRegion] = useState('us-ashburn-1');
  const [ociPrivateKey, setOciPrivateKey] = useState('');
  const [ociProfile, setOciProfile] = useState('DEFAULT');

  // File Upload
  const [uploadedFileName, setUploadedFileName] = useState('');
  const [uploadedFileContent, setUploadedFileContent] = useState('');

  const fetchCredentials = async () => {
    try {
      setLoading(true);
      const data = await credentialsApi.list();
      setCredentials(data);
    } catch (err) {
      console.error("Failed to load credentials:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCredentials();
  }, []);

  const handleProviderChange = (newProvider) => {
    setProvider(newProvider);
    const availableAuth = PROVIDER_AUTH_MODES[newProvider] || [];
    if (availableAuth.length > 0) {
      setAuthType(availableAuth[0].id);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploadedFileName(file.name);
    const reader = new FileReader();
    reader.onload = (event) => {
      setUploadedFileContent(event.target.result);
    };
    reader.readAsText(file);
  };

  const resetForm = () => {
    setName('');
    setProvider('aws');
    setAuthType('keys');
    setAwsAccessKey('');
    setAwsSecretKey('');
    setAwsSessionToken('');
    setAwsProfile('');
    setAzureTenantId('');
    setAzureClientId('');
    setAzureClientSecret('');
    setAzureUsername('');
    setAzurePassword('');
    setAzureSubscriptions('');
    setAzureAllSubscriptions(false);
    setGcpProjectId('');
    setGcpFolderId('');
    setGcpOrgId('');
    setGcpAllProjects(false);
    setK8sContext('');
    setK8sClusterProvider('');
    setK8sSubscriptionId('');
    setAliyunAccessKeyId('');
    setAliyunAccessKeySecret('');
    setDoToken('');
    setDoAccessKey('');
    setDoAccessSecret('');
    setOciUserOcid('');
    setOciTenancyOcid('');
    setOciFingerprint('');
    setOciRegion('us-ashburn-1');
    setOciPrivateKey('');
    setOciProfile('DEFAULT');
    setUploadedFileName('');
    setUploadedFileContent('');
    setError('');
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setError('');

    let credData = {};

    if (provider === 'aws') {
      if (authType === 'keys') {
        credData = {
          aws_access_key_id: awsAccessKey,
          aws_secret_access_key: awsSecretKey,
          aws_session_token: awsSessionToken || undefined,
        };
      } else {
        credData = { profile: awsProfile || 'default' };
      }
    } else if (provider === 'azure') {
      credData = {
        tenant_id: azureTenantId || undefined,
        client_id: azureClientId || undefined,
        client_secret: azureClientSecret || undefined,
        username: azureUsername || undefined,
        password: azurePassword || undefined,
        subscription_ids: azureSubscriptions ? azureSubscriptions.split(',').map(s => s.trim()).filter(Boolean) : undefined,
        all_subscriptions: azureAllSubscriptions || undefined,
      };
    } else if (provider === 'gcp') {
      credData = {
        project_id: gcpProjectId || undefined,
        folder_id: gcpFolderId || undefined,
        organization_id: gcpOrgId || undefined,
        all_projects: gcpAllProjects || undefined,
      };
    } else if (provider === 'kubernetes') {
      credData = {
        kubernetes_context: k8sContext || undefined,
        kubernetes_cluster_provider: k8sClusterProvider || undefined,
        kubernetes_azure_subscription_id: k8sSubscriptionId || undefined,
      };
    } else if (provider === 'aliyun') {
      credData = {
        access_key_id: aliyunAccessKeyId,
        access_key_secret: aliyunAccessKeySecret,
      };
    } else if (provider === 'do') {
      credData = {
        token: doToken || undefined,
        access_key: doAccessKey || undefined,
        access_secret: doAccessSecret || undefined,
      };
    } else if (provider === 'oci') {
      if (authType === 'direct') {
        credData = {
          user: ociUserOcid,
          tenancy: ociTenancyOcid,
          fingerprint: ociFingerprint,
          region: ociRegion || 'us-ashburn-1',
          private_key_content: ociPrivateKey,
          profile: ociProfile || 'DEFAULT',
        };
      } else {
        credData = {
          profile: ociProfile || 'DEFAULT',
        };
      }
    }

    const payload = {
      name,
      provider,
      auth_type: authType,
      data: credData,
      raw_file_content: uploadedFileContent || undefined,
      file_name: uploadedFileName || undefined,
    };

    try {
      await credentialsApi.create(payload);
      setShowModal(false);
      resetForm();
      fetchCredentials();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save credential.');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Are you sure you want to delete this credential profile?")) return;
    try {
      await credentialsApi.delete(id);
      fetchCredentials();
    } catch (err) {
      alert("Failed to delete credential");
    }
  };

  const filteredCredentials = selectedFilter === 'all'
    ? credentials
    : credentials.filter(c => c.provider === selectedFilter);

  const availableAuthModes = PROVIDER_AUTH_MODES[provider] || [];

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-dark-card border border-dark-border p-6 rounded-2xl">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Credentials & Profile Vault</h2>
          <p className="text-sm text-slate-400 mt-1">
            Store and manage cloud authentication keys and profiles for one-click security assessments.
          </p>
        </div>
        <button
          onClick={() => { resetForm(); setShowModal(true); }}
          className="flex items-center gap-2 bg-brand-500 hover:bg-brand-600 text-slate-950 font-semibold px-4 py-2.5 rounded-xl shadow-lg shadow-brand-500/20 transition cursor-pointer"
        >
          <Plus className="w-5 h-5" />
          <span>Add Credential Profile</span>
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
        <span className="text-slate-500 flex items-center gap-1 mr-2"><Filter className="w-3.5 h-3.5" /> Filter:</span>
        {['all', 'aws', 'azure', 'gcp', 'kubernetes', 'aliyun', 'do', 'oci'].map((prov) => (
          <button
            key={prov}
            onClick={() => setSelectedFilter(prov)}
            className={`px-3 py-1.5 rounded-xl font-medium transition uppercase ${
              selectedFilter === prov
                ? 'bg-brand-500 text-slate-950 font-bold shadow'
                : 'bg-dark-card border border-dark-border text-slate-400 hover:text-white'
            }`}
          >
            {prov}
          </button>
        ))}
      </div>

      {/* Grid of Credentials */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredCredentials.length === 0 ? (
          <div className="col-span-full bg-dark-card border border-dark-border border-dashed p-12 rounded-2xl text-center space-y-3">
            <Lock className="w-10 h-10 text-slate-600 mx-auto" />
            <h3 className="text-base font-semibold text-white">No Stored Profiles Found</h3>
            <p className="text-sm text-slate-400 max-w-md mx-auto">
              Securely store your cloud access credentials (AWS, Azure Service Principal, Azure CLI, GCP Service Account, etc.) for instant re-use during security audits.
            </p>
          </div>
        ) : (
          filteredCredentials.map((cred) => (
            <div key={cred.id} className="bg-dark-card border border-dark-border p-5 rounded-2xl shadow-lg flex flex-col justify-between space-y-4">
              <div>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded text-xs font-mono font-bold uppercase bg-brand-500/10 text-brand-400 border border-brand-500/20">
                      {cred.provider}
                    </span>
                    <span className="text-xs text-slate-400 font-mono">• {cred.auth_type}</span>
                  </div>
                  <button
                    onClick={() => handleDelete(cred.id)}
                    className="text-slate-500 hover:text-red-400 p-1 rounded-lg hover:bg-red-500/10 transition cursor-pointer"
                    title="Delete"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                <h3 className="text-base font-semibold text-white mt-3">{cred.name}</h3>

                {/* Summary of masked data */}
                <div className="mt-3 bg-dark-bg/60 p-3 rounded-xl border border-dark-border text-xs font-mono space-y-1 text-slate-400">
                  {Object.entries(cred.data_summary || {}).map(([k, v]) => (
                    <div key={k} className="flex justify-between overflow-hidden">
                      <span className="text-slate-500 truncate mr-2">{k}:</span>
                      <span className="text-slate-300 truncate">{String(v)}</span>
                    </div>
                  ))}
                  {cred.has_file && (
                    <div className="flex items-center gap-1 text-brand-400 text-[11px] pt-1 font-sans">
                      <FileText className="w-3.5 h-3.5" /> File Attachment Stored
                    </div>
                  )}
                </div>
              </div>

              <div className="text-[11px] text-slate-500 border-t border-dark-border/60 pt-3">
                Saved: {new Date(cred.created_at).toLocaleDateString()}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Add Credential Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-dark-card border border-dark-border rounded-2xl w-full max-w-lg p-6 shadow-2xl space-y-5 my-8">
            <div className="flex items-center justify-between border-b border-dark-border pb-4">
              <h3 className="text-lg font-bold text-white">Save New Credential Profile</h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white cursor-pointer">✕</button>
            </div>

            {error && (
              <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-xs text-red-400">
                {error}
              </div>
            )}

            <form onSubmit={handleSave} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-300 font-semibold mb-1">Profile Name *</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Azure Production SP / AWS ReadOnly"
                  className="w-full bg-dark-bg border border-dark-border rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Cloud Provider</label>
                  <select
                    value={provider}
                    onChange={(e) => handleProviderChange(e.target.value)}
                    className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                  >
                    <option value="aws">Amazon Web Services (AWS)</option>
                    <option value="azure">Microsoft Azure</option>
                    <option value="gcp">Google Cloud Platform (GCP)</option>
                    <option value="kubernetes">Kubernetes</option>
                    <option value="aliyun">Alibaba Cloud (Aliyun)</option>
                    <option value="do">DigitalOcean</option>
                    <option value="oci">Oracle Cloud (OCI)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Authentication Method</label>
                  <select
                    value={authType}
                    onChange={(e) => setAuthType(e.target.value)}
                    className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                  >
                    {availableAuthModes.map((m) => (
                      <option key={m.id} value={m.id}>{m.label}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* AWS Form */}
              {provider === 'aws' && authType === 'keys' && (
                <div className="space-y-3 pt-2">
                  <div>
                    <label className="block text-slate-400 mb-1">AWS Access Key ID *</label>
                    <input
                      type="text"
                      required
                      value={awsAccessKey}
                      onChange={(e) => setAwsAccessKey(e.target.value)}
                      placeholder="AKIAIOSFODNN7EXAMPLE"
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">AWS Secret Access Key *</label>
                    <input
                      type="password"
                      required
                      value={awsSecretKey}
                      onChange={(e) => setAwsSecretKey(e.target.value)}
                      placeholder="Secret Key"
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">AWS Session Token (Optional)</label>
                    <input
                      type="text"
                      value={awsSessionToken}
                      onChange={(e) => setAwsSessionToken(e.target.value)}
                      placeholder="AQoDYXdzEJr..."
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    />
                  </div>
                </div>
              )}

              {provider === 'aws' && authType === 'profile' && (
                <div className="pt-2">
                  <label className="block text-slate-400 mb-1">Profile Name (in ~/.aws/credentials) *</label>
                  <input
                    type="text"
                    required
                    value={awsProfile}
                    onChange={(e) => setAwsProfile(e.target.value)}
                    placeholder="default"
                    className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                  />
                </div>
              )}

              {/* Azure Form */}
              {provider === 'azure' && (
                <div className="space-y-3 pt-2">
                  {authType === 'service_principal' && (
                    <>
                      <div>
                        <label className="block text-slate-400 mb-1">Tenant ID (Directory ID) *</label>
                        <input
                          type="text"
                          required
                          value={azureTenantId}
                          onChange={(e) => setAzureTenantId(e.target.value)}
                          placeholder="00000000-0000-0000-0000-000000000000"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-slate-400 mb-1">Client ID (Application ID) *</label>
                        <input
                          type="text"
                          required
                          value={azureClientId}
                          onChange={(e) => setAzureClientId(e.target.value)}
                          placeholder="00000000-0000-0000-0000-000000000000"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-slate-400 mb-1">Client Secret *</label>
                        <input
                          type="password"
                          required
                          value={azureClientSecret}
                          onChange={(e) => setAzureClientSecret(e.target.value)}
                          placeholder="Secret value"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                    </>
                  )}

                  {authType === 'user_account' && (
                    <>
                      <div>
                        <label className="block text-slate-400 mb-1">Tenant ID (Directory ID) *</label>
                        <input
                          type="text"
                          required
                          value={azureTenantId}
                          onChange={(e) => setAzureTenantId(e.target.value)}
                          placeholder="00000000-0000-0000-0000-000000000000"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-slate-400 mb-1">Azure Username / Email *</label>
                        <input
                          type="text"
                          required
                          value={azureUsername}
                          onChange={(e) => setAzureUsername(e.target.value)}
                          placeholder="admin@contoso.onmicrosoft.com"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-slate-400 mb-1">Azure Password *</label>
                        <input
                          type="password"
                          required
                          value={azurePassword}
                          onChange={(e) => setAzurePassword(e.target.value)}
                          placeholder="Account password"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                    </>
                  )}

                  {authType === 'user_account_browser' && (
                    <div>
                      <label className="block text-slate-400 mb-1">Tenant ID (Directory ID) *</label>
                      <input
                        type="text"
                        required
                        value={azureTenantId}
                        onChange={(e) => setAzureTenantId(e.target.value)}
                        placeholder="00000000-0000-0000-0000-000000000000"
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                    </div>
                  )}

                  {authType === 'file_auth' && (
                    <div className="space-y-2">
                      <label className="block text-slate-400 mb-1">Upload SDK Auth JSON File *</label>
                      <input
                        type="file"
                        accept=".json"
                        required
                        onChange={handleFileUpload}
                        className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-500/10 file:text-brand-400 hover:file:bg-brand-500/20"
                      />
                    </div>
                  )}

                  {authType === 'cli' && (
                    <p className="text-xs text-slate-400 bg-dark-bg/60 p-3 rounded-xl border border-dark-border">
                      Uses the active Azure CLI (<code className="text-brand-400">az login</code>) session inside the server environment.
                    </p>
                  )}

                  {authType === 'msi' && (
                    <p className="text-xs text-slate-400 bg-dark-bg/60 p-3 rounded-xl border border-dark-border">
                      Uses Managed Service Identity (MSI) available when running inside Azure VM or Container.
                    </p>
                  )}

                  {/* Scope: Subscriptions */}
                  <div className="pt-2 border-t border-dark-border/60">
                    <label className="block text-slate-400 mb-1">Target Subscription ID(s) (Optional, comma-separated)</label>
                    <input
                      type="text"
                      disabled={azureAllSubscriptions}
                      value={azureSubscriptions}
                      onChange={(e) => setAzureSubscriptions(e.target.value)}
                      placeholder="e.g. sub-id-1, sub-id-2 (leave blank for default)"
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none disabled:opacity-50"
                    />
                    <label className="flex items-center gap-2 mt-2 text-slate-400 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={azureAllSubscriptions}
                        onChange={(e) => setAzureAllSubscriptions(e.target.checked)}
                        className="accent-brand-500"
                      />
                      <span>Scan All Accessible Subscriptions</span>
                    </label>
                  </div>
                </div>
              )}

              {/* GCP Form */}
              {provider === 'gcp' && (
                <div className="space-y-3 pt-2">
                  {authType === 'service_account' && (
                    <div className="space-y-2">
                      <label className="block text-slate-400 mb-1">Service Account Key JSON File *</label>
                      <input
                        type="file"
                        accept=".json"
                        required
                        onChange={handleFileUpload}
                        className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-500/10 file:text-brand-400 hover:file:bg-brand-500/20"
                      />
                    </div>
                  )}

                  {authType === 'user_account' && (
                    <p className="text-xs text-slate-400 bg-dark-bg/60 p-3 rounded-xl border border-dark-border">
                      Uses gcloud user authentication credentials in the environment.
                    </p>
                  )}

                  <div>
                    <label className="block text-slate-400 mb-1">GCP Project ID (Optional)</label>
                    <input
                      type="text"
                      value={gcpProjectId}
                      onChange={(e) => setGcpProjectId(e.target.value)}
                      placeholder="my-gcp-project-123"
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Folder ID (Optional)</label>
                    <input
                      type="text"
                      value={gcpFolderId}
                      onChange={(e) => setGcpFolderId(e.target.value)}
                      placeholder="123456789012"
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Organization ID (Optional)</label>
                    <input
                      type="text"
                      value={gcpOrgId}
                      onChange={(e) => setGcpOrgId(e.target.value)}
                      placeholder="123456789012"
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    />
                  </div>
                  <label className="flex items-center gap-2 mt-2 text-slate-400 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={gcpAllProjects}
                      onChange={(e) => setGcpAllProjects(e.target.checked)}
                      className="accent-brand-500"
                    />
                    <span>Scan All Accessible Projects</span>
                  </label>
                </div>
              )}

              {/* Kubernetes Form */}
              {provider === 'kubernetes' && (
                <div className="space-y-3 pt-2">
                  {authType === 'config_file' && (
                    <div className="space-y-2">
                      <label className="block text-slate-400 mb-1">Kubeconfig File *</label>
                      <input
                        type="file"
                        required
                        onChange={handleFileUpload}
                        className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-500/10 file:text-brand-400 hover:file:bg-brand-500/20"
                      />
                    </div>
                  )}
                  <div>
                    <label className="block text-slate-400 mb-1">Cluster Provider (Optional)</label>
                    <select
                      value={k8sClusterProvider}
                      onChange={(e) => setK8sClusterProvider(e.target.value)}
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    >
                      <option value="">Generic / Default</option>
                      <option value="aks">Azure Kubernetes Service (AKS)</option>
                      <option value="eks">Amazon Elastic Kubernetes Service (EKS)</option>
                      <option value="gke">Google Kubernetes Engine (GKE)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Context Name (Optional)</label>
                    <input
                      type="text"
                      value={k8sContext}
                      onChange={(e) => setK8sContext(e.target.value)}
                      placeholder="e.g. cluster-admin-context"
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    />
                  </div>
                  {k8sClusterProvider === 'aks' && (
                    <div>
                      <label className="block text-slate-400 mb-1">Azure Subscription ID (for AKS)</label>
                      <input
                        type="text"
                        value={k8sSubscriptionId}
                        onChange={(e) => setK8sSubscriptionId(e.target.value)}
                        placeholder="00000000-0000-0000-0000-000000000000"
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                    </div>
                  )}
                </div>
              )}

              {/* Aliyun Form */}
              {provider === 'aliyun' && (
                <div className="space-y-3 pt-2">
                  <div>
                    <label className="block text-slate-400 mb-1">Aliyun Access Key ID *</label>
                    <input
                      type="text"
                      required
                      value={aliyunAccessKeyId}
                      onChange={(e) => setAliyunAccessKeyId(e.target.value)}
                      placeholder="LTAI..."
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Aliyun Access Key Secret *</label>
                    <input
                      type="password"
                      required
                      value={aliyunAccessKeySecret}
                      onChange={(e) => setAliyunAccessKeySecret(e.target.value)}
                      placeholder="Access Key Secret"
                      className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                    />
                  </div>
                </div>
              )}

              {/* DigitalOcean Form */}
              {provider === 'do' && (
                <div className="space-y-3 pt-2">
                  {(authType === 'token' || authType === 'both') && (
                    <div>
                      <label className="block text-slate-400 mb-1">DO API Personal Access Token *</label>
                      <input
                        type="password"
                        required={authType === 'token'}
                        value={doToken}
                        onChange={(e) => setDoToken(e.target.value)}
                        placeholder="dop_v1_..."
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                    </div>
                  )}
                  {(authType === 'spaces' || authType === 'both') && (
                    <>
                      <div>
                        <label className="block text-slate-400 mb-1">Spaces Access Key *</label>
                        <input
                          type="text"
                          required={authType === 'spaces'}
                          value={doAccessKey}
                          onChange={(e) => setDoAccessKey(e.target.value)}
                          placeholder="DO Spaces Key"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-slate-400 mb-1">Spaces Secret Key *</label>
                        <input
                          type="password"
                          required={authType === 'spaces'}
                          value={doAccessSecret}
                          onChange={(e) => setDoAccessSecret(e.target.value)}
                          placeholder="DO Spaces Secret"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                    </>
                  )}
                </div>
              )}

              {/* OCI Form */}
              {provider === 'oci' && (
                <div className="space-y-3 pt-2">
                  {authType === 'direct' && (
                    <>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                          <label className="block text-slate-400 mb-1">User OCID *</label>
                          <input
                            type="text"
                            required
                            value={ociUserOcid}
                            onChange={(e) => setOciUserOcid(e.target.value)}
                            placeholder="ocid1.user.oc1..aaaa..."
                            className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                          />
                        </div>
                        <div>
                          <label className="block text-slate-400 mb-1">Tenancy OCID *</label>
                          <input
                            type="text"
                            required
                            value={ociTenancyOcid}
                            onChange={(e) => setOciTenancyOcid(e.target.value)}
                            placeholder="ocid1.tenancy.oc1..aaaa..."
                            className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                          />
                        </div>
                        <div>
                          <label className="block text-slate-400 mb-1">API Key Fingerprint *</label>
                          <input
                            type="text"
                            required
                            value={ociFingerprint}
                            onChange={(e) => setOciFingerprint(e.target.value)}
                            placeholder="20:3b:97:13:55:1c:..."
                            className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none font-mono text-xs"
                          />
                        </div>
                        <div>
                          <label className="block text-slate-400 mb-1">OCI Region *</label>
                          <input
                            type="text"
                            required
                            value={ociRegion}
                            onChange={(e) => setOciRegion(e.target.value)}
                            placeholder="us-ashburn-1"
                            className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                          />
                        </div>
                      </div>
                      <div>
                        <label className="block text-slate-400 mb-1">API Private Key (PEM format) *</label>
                        <textarea
                          rows={3}
                          required
                          value={ociPrivateKey}
                          onChange={(e) => setOciPrivateKey(e.target.value)}
                          placeholder="-----BEGIN RSA PRIVATE KEY-----&#10;...&#10;-----END RSA PRIVATE KEY-----"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl p-3 text-xs text-slate-200 font-mono focus:border-brand-500 focus:outline-none leading-relaxed"
                        />
                      </div>
                    </>
                  )}

                  {authType === 'config_file' && (
                    <div className="space-y-3">
                      <div>
                        <label className="block text-slate-400 mb-1">Upload OCI Config File (~/.oci/config) *</label>
                        <input
                          type="file"
                          required
                          onChange={handleFileUpload}
                          className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-500/10 file:text-brand-400 hover:file:bg-brand-500/20"
                        />
                      </div>
                      <div>
                        <label className="block text-slate-400 mb-1">Profile Name in Config (Optional)</label>
                        <input
                          type="text"
                          value={ociProfile}
                          onChange={(e) => setOciProfile(e.target.value)}
                          placeholder="DEFAULT"
                          className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                        />
                      </div>
                    </div>
                  )}

                  {authType === 'profile' && (
                    <div>
                      <label className="block text-slate-400 mb-1">OCI Profile Name (in ~/.oci/config) *</label>
                      <input
                        type="text"
                        required
                        value={ociProfile}
                        onChange={(e) => setOciProfile(e.target.value)}
                        placeholder="DEFAULT"
                        className="w-full bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
                      />
                    </div>
                  )}
                </div>
              )}

              <div className="flex justify-end gap-3 pt-4 border-t border-dark-border">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-sm text-slate-400 hover:text-white cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-brand-500 hover:bg-brand-600 text-slate-950 font-semibold px-4 py-2 rounded-xl text-sm transition cursor-pointer"
                >
                  Save Profile
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
