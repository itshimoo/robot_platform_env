// Simple RobotLab Web GUI
document.addEventListener('DOMContentLoaded', function() {
    console.log('RobotLab Web GUI loaded');
    
    // Simple API functions
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
    
    // Update status display
    async function updateStatus() {
        const result = await apiCall('status');
        const statusDiv = document.getElementById('status');
        
        if (result.success) {
            statusDiv.innerHTML = `<pre>${result.data}</pre>`;
        } else {
            statusDiv.innerHTML = `<p class="error">Error: ${result.error}</p>`;
        }
    }
    
    // Button click handlers
    window.buildContainer = async function() {
        const result = await apiCall('build', 'POST');
        if (result.success) {
            alert('Build completed successfully!');
            updateStatus();
        } else {
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
    loadLogs();
}); 