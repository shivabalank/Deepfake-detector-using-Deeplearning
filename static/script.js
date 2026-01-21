const uploadSection = document.getElementById('upload-section');
const loadingSection = document.getElementById('loading-section');
const resultSection = document.getElementById('result-section');
const fileInput = document.getElementById('file-input');
const dropZone = document.getElementById('drop-zone');
const detectBtn = document.getElementById('detect-btn');
const progressBar = document.getElementById('progress-bar');
const progressText = document.getElementById('progress-text');
let selectedFile = null;

dropZone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        selectedFile = e.target.files[0];
        document.querySelector('.upload-area h3').innerText = selectedFile.name;
        detectBtn.style.background = "#4A90E2";
        detectBtn.style.color = "white";
    }
});

detectBtn.addEventListener('click', () => {
    if (!selectedFile) { alert("Please select a file first!"); return; }
    uploadSection.style.display = 'none';
    loadingSection.style.display = 'block';
    let width = 0;
    const interval = setInterval(() => {
        if (width >= 90) {
            clearInterval(interval);
            uploadFile(selectedFile);
        } else {
            width++;
            progressBar.style.width = width + '%';
            progressText.innerText = `Analyzing... ${width}%`;
        }
    }, 30);
});

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    fetch('/detect', { method: 'POST', body: formData })
    .then(response => response.json())
    .then(data => {
        progressBar.style.width = '100%';
        setTimeout(() => { showResults(data); }, 500);
    })
    .catch(error => { console.error(error); alert("Error detecting."); location.reload(); });
}

function showResults(data) {
    loadingSection.style.display = 'none';
    resultSection.style.display = 'block';
    const result = data.result;
    const isFake = result.is_fake;
    
    const statusBox = document.getElementById('status-box');
    statusBox.innerHTML = `<h3>${result.label}</h3>`;
    statusBox.className = isFake ? 'status-box danger' : 'status-box success';
    
    document.getElementById('center-percent').innerText = result.ai_probability + '%';
    document.getElementById('val-ai').innerText = result.ai_probability + '%';
    document.getElementById('val-organic').innerText = result.organic_probability + '%';

    new Chart(document.getElementById('probabilityChart').getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['AI Generated', 'Organic'],
            datasets: [{
                data: [result.ai_probability, result.organic_probability],
                backgroundColor: [isFake ? '#ff4d4d' : '#4A90E2', '#89ec91'],
                borderWidth: 0
            }]
        },
        options: { cutout: '80%', responsive: true, plugins: { legend: { display: false } } }
    });
    
    document.getElementById('media-preview').innerHTML = `<img src="/static/uploads/${data.filename}" alt="Analyzed Media">`;
}
