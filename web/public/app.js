// Professional RobotLab Web GUI
document.addEventListener('DOMContentLoaded', function() {
    console.log('🤖 RobotLab Web GUI loaded');
    
    // Add loading animation
    function showLoading(element) {
        element.innerHTML = '<div class="loading"></div> Loading...';
    }
    
    // Add success animation
    function showSuccess(element, message) {
        element.innerHTML = `<span class="status-indicator success"></span> ${message}`;
        setTimeout(() => {
            updateStatus();
        }, 1000);
    }
    
    // Professional API functions
    async function apiCall(endpoint, method = 'GET', data = null) {
        try {
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                }
            };
            
            if (data) {
                options.body = JSON.stringify(data);
            }
            
            const response = await fetch(`/api/${endpoint}`, options);
            const result = await response.json();
            return result;
        } catch (error) {
            console.error('API call failed:', error);
            return { success: false, error: error.message };
        }
    }
    
    // Update status display with professional styling
    async function updateStatus() {
        const statusDiv = document.getElementById('status');
        showLoading(statusDiv);
        
        const result = await apiCall('status');
        
        if (result.success) {
            statusDiv.innerHTML = `<pre>${result.data}</pre>`;
        } else {
            statusDiv.innerHTML = `<p class="error">❌ Error: ${result.error}</p>`;
        }
    }

    // Update configuration display with professional styling
    async function updateConfig() {
        const configDiv = document.getElementById('config');
        showLoading(configDiv);
        
        const result = await apiCall('config');
        
        if (result.success) {
            configDiv.innerHTML = `<pre>${result.data}</pre>`;
        } else {
            configDiv.innerHTML = `<p class="error">❌ Error: ${result.error}</p>`;
        }
    }

    // Update GPU status with professional styling
    async function updateGPUStatus() {
        const gpuStatusDiv = document.getElementById('gpu-status');
        showLoading(gpuStatusDiv);
        
        const result = await apiCall('config');
        
        if (result.success) {
            // Extract GPU status from config output
            const gpuEnabled = result.data.includes('🚀 GPU Support: ENABLED');
            const gpuDisabled = result.data.includes('💻 GPU Support: DISABLED');
            
            if (gpuEnabled) {
                gpuStatusDiv.innerHTML = `<p style="color: var(--success-color); font-weight: 600;">🚀 GPU Support: ENABLED (AI workloads ready)</p>`;
            } else if (gpuDisabled) {
                gpuStatusDiv.innerHTML = `<p style="color: var(--text-secondary); font-weight: 600;">💻 GPU Support: DISABLED (CPU-only mode)</p>`;
            } else {
                gpuStatusDiv.innerHTML = `<p>Loading GPU status...</p>`;
            }
        } else {
            gpuStatusDiv.innerHTML = `<p class="error">❌ Error: ${result.error}</p>`;
        }
    }
    
    // Button click handlers
    window.buildContainer = async function() {
        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '<div class="loading"></div> Building...';
        button.disabled = true;
        
        const result = await apiCall('build', 'POST');
        if (result.success) {
            button.innerHTML = '<span class="status-indicator success"></span> Build Complete';
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 2000);
            updateStatus();
        } else {
            button.innerHTML = '<span class="status-indicator danger"></span> Build Failed';
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 3000);
            alert('Build failed: ' + result.error);
        }
    };
    
    window.runContainer = async function() {
        const result = await apiCall('run', 'POST');
        if (result.success) {
            alert('Container started successfully!');
            updateStatus();
        } else {
            alert('Failed to start container: ' + result.error);
        }
    };
    
    window.stopContainer = async function() {
        const result = await apiCall('stop', 'POST');
        if (result.success) {
            alert('Container stopped successfully!');
            updateStatus();
        } else {
            alert('Failed to stop container: ' + result.error);
        }
    };

    window.cleanContainer = async function() {
        const result = await apiCall('clean', 'POST');
        if (result.success) {
            alert('Container cleaned successfully!');
            updateStatus();
        } else {
            alert('Failed to clean container: ' + result.error);
        }
    };

    window.toggleGPU = async function() {
        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '<div class="loading"></div> Toggling...';
        button.disabled = true;
        
        const result = await apiCall('gpu', 'POST');
        if (result.success) {
            button.innerHTML = '<span class="status-indicator success"></span> GPU Toggled';
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 2000);
            updateStatus();
            updateGPUStatus();
            updateConfig();
        } else {
            button.innerHTML = '<span class="status-indicator danger"></span> Toggle Failed';
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 3000);
            alert('Failed to toggle GPU: ' + result.error);
        }
    };

    window.openShell = async function() {
        const result = await apiCall('shell', 'POST');
        if (result.success) {
            alert('Shell opened successfully! Check your terminal.');
            updateStatus();
        } else {
            alert('Failed to open shell: ' + result.error);
        }
    };

    window.updateConfig = async function() {
        const result = await apiCall('update', 'POST');
        if (result.success) {
            alert('Configuration updated successfully!');
            updateStatus();
            updateConfig();
            updateGPUStatus();
        } else {
            alert('Failed to update configuration: ' + result.error);
        }
    };
    
    window.executeCommand = async function() {
        const command = document.getElementById('commandInput').value;
        if (!command) {
            alert('Please enter a command');
            return;
        }
        
        const result = await apiCall('exec', 'POST', { command: command });
        const outputDiv = document.getElementById('output');
        
        if (result.success) {
            outputDiv.innerHTML = `<pre>${result.data}</pre>`;
        } else {
            outputDiv.innerHTML = `<p class="error">Error: ${result.error}</p>`;
        }
        
        document.getElementById('commandInput').value = '';
    };
    
    window.loadLogs = async function() {
        const result = await apiCall('logs');
        const logsDiv = document.getElementById('logs');
        
        if (result.success) {
            logsDiv.innerHTML = `<pre>${result.data}</pre>`;
        } else {
            logsDiv.innerHTML = `<p class="error">Error: ${result.error}</p>`;
        }
    };
    
    // Load initial data
    updateStatus();
    updateConfig();
    updateGPUStatus();
    loadLogs();
}); 