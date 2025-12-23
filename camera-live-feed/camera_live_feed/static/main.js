// Camera Live Feed - Main JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const videoFeed = document.getElementById('video-feed');
    const loading = document.getElementById('loading');
    const status = document.getElementById('status');
    const statusText = document.getElementById('status-text');
    const snapshotBtn = document.getElementById('snapshot-btn');

    // Handle video feed load
    videoFeed.onload = () => {
        loading.classList.add('hidden');
        status.classList.remove('error');
        status.classList.add('live');
        statusText.textContent = 'Live';
    };

    videoFeed.onerror = () => {
        loading.classList.remove('hidden');
        status.classList.remove('live');
        status.classList.add('error');
        statusText.textContent = 'Connection lost';

        // Retry connection after 2 seconds
        setTimeout(() => {
            videoFeed.src = 'api/stream?' + Date.now();
            statusText.textContent = 'Reconnecting...';
        }, 2000);
    };

    // Snapshot functionality
    snapshotBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('api/snapshot');
            if (!response.ok) throw new Error('Failed to capture');

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            // Create download link
            const a = document.createElement('a');
            a.href = url;
            a.download = `reachy-mini-snapshot-${Date.now()}.jpg`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            // Visual feedback
            snapshotBtn.style.background = 'rgba(0, 255, 136, 0.2)';
            setTimeout(() => {
                snapshotBtn.style.background = '';
            }, 200);

        } catch (error) {
            console.error('Snapshot error:', error);
            snapshotBtn.style.background = 'rgba(255, 68, 68, 0.2)';
            setTimeout(() => {
                snapshotBtn.style.background = '';
            }, 200);
        }
    });

    // Check status periodically
    async function checkStatus() {
        try {
            const response = await fetch('api/status');
            if (response.ok) {
                const data = await response.json();
                if (data.streaming) {
                    status.classList.add('live');
                    status.classList.remove('error');
                    statusText.textContent = `Live (${data.fps} FPS)`;
                }
            }
        } catch (error) {
            // Silently fail - video feed error handler will catch issues
        }
    }

    // Check status every 5 seconds
    setInterval(checkStatus, 5000);
});
