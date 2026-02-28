document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('logoForm');
    const svgContainer = document.getElementById('svgContainer');
    const saveBtn = document.getElementById('saveBtn');
    const autoGenerateToggle = document.getElementById('autoGenerateToggle');
    const textInput = document.getElementById('textInput');
    let currentSvgBlob = null;

    const triggerAutoGenerate = () => {
        if (autoGenerateToggle && autoGenerateToggle.checked && textInput.value.trim() !== '') {
            form.requestSubmit();
        }
    };

    const settingInputs = form.querySelectorAll('input[type="radio"], input[type="checkbox"]:not(#autoGenerateToggle)');
    settingInputs.forEach(input => {
        input.addEventListener('change', triggerAutoGenerate);
    });

    const savePngBtn = document.getElementById('savePngBtn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const payload = {
            text: formData.get('text'),
            mode: formData.get('mode'),
            add_frame: formData.get('add_frame') === 'on',
            add_text: formData.get('add_text') === 'on',
            random_colors: formData.get('random_colors') === 'on',
            empty_spaces: formData.get('empty_spaces') === 'on',
            transparent_background: formData.get('transparent_background') === 'on',
            transparent_text: formData.get('transparent_text') === 'on',
        };

        if (!payload.text) return;

        const generateBtn = form.querySelector('.generate-btn');
        const originalText = generateBtn.innerHTML;
        generateBtn.innerHTML = '<span>Generating...</span>';
        generateBtn.disabled = true;
        svgContainer.classList.add('loading');

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || 'Failed to generate logo');
            }

            const svgText = await response.text();

            // Render SVG
            svgContainer.innerHTML = svgText;
            svgContainer.classList.remove('loading');

            // Store Blob for saving
            currentSvgBlob = new Blob([svgText], { type: 'image/svg+xml' });
            saveBtn.disabled = false;
            savePngBtn.disabled = false;

        } catch (error) {
            console.error('Error:', error);
            alert('Failed to generate logo: ' + error.message);
            svgContainer.classList.remove('loading');
        } finally {
            generateBtn.innerHTML = originalText;
            generateBtn.disabled = false;
        }
    });

    saveBtn.addEventListener('click', () => {
        if (!currentSvgBlob) return;

        const url = URL.createObjectURL(currentSvgBlob);
        const a = document.createElement('a');
        a.href = url;

        const textVal = document.getElementById('textInput').value.trim() || 'logo';
        const sanitized = textVal.replace(/[^a-z0-9]/gi, '_').toLowerCase();

        a.download = `${sanitized}_logo.svg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    savePngBtn.addEventListener('click', () => {
        if (!currentSvgBlob) return;

        const url = URL.createObjectURL(currentSvgBlob);
        const img = new Image();

        img.onload = () => {
            const canvas = document.createElement('canvas');
            // Assuming default dimensions if not set on SVG, or we can get it from the container
            const svgElement = svgContainer.querySelector('svg');
            let width = 800;
            let height = 800;
            if (svgElement) {
                const rect = svgElement.getBoundingClientRect();
                width = rect.width * 2; // high res
                height = rect.height * 2;
            }

            canvas.width = width;
            canvas.height = height;

            const ctx = canvas.getContext('2d');

            // Fill background unless transparent background is requested
            const isTransparent = document.querySelector('input[name="transparent_background"]').checked;
            if (!isTransparent) {
                ctx.fillStyle = '#0f1115'; // Match var(--bg-dark)
                ctx.fillRect(0, 0, width, height);
            }

            ctx.drawImage(img, 0, 0, width, height);

            const pngUrl = canvas.toDataURL('image/png');
            const a = document.createElement('a');
            a.href = pngUrl;

            const textVal = document.getElementById('textInput').value.trim() || 'logo';
            const sanitized = textVal.replace(/[^a-z0-9]/gi, '_').toLowerCase();

            a.download = `${sanitized}_logo.png`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);

            URL.revokeObjectURL(url);
        };

        img.src = url;
    });
});
