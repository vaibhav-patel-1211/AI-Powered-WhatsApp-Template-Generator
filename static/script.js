const $ = id => document.getElementById(id);
let buttons = [];

// Real-time Preview Engine
const updatePreview = () => {
    const hVal = $('hInput').value;
    $('pH').innerText = hVal;
    $('pH').classList.toggle('hidden', !hVal);
    
    $('pB').innerHTML = formatWA($('bInput').value);
    
    $('pBtns').innerHTML = buttons.map(b => `
        <div class="wa-btn">
            <i class="fas fa-${b.type === 'url' ? 'external-link-alt' : 'reply'}" style="font-size: 0.8rem; opacity: 0.6;"></i>
            ${b.text || 'Button'}
        </div>
    `).join('');
};

const formatWA = (t) => {
    if (!t) return "";
    return t.replace(/\*([^*]+)\*/g, '<b>$1</b>')
            .replace(/_([^_]+)_/g, '<i>$1</i>')
            .replace(/~([^~]+)~/g, '<s>$1</s>')
            .replace(/\n/g, '<br>');
};

// State Management
window.uBtn = (i, k, v) => { 
    buttons[i][k] = v; 
    if(k === 'type') renderBtnEditor(); 
    updatePreview(); 
};

window.rBtn = (i) => { 
    buttons.splice(i, 1); 
    renderBtnEditor(); 
};

const renderBtnEditor = () => {
    $('btnList').innerHTML = buttons.map((b, i) => `
        <div class="action-card">
            <div class="action-card-main">
                <select onchange="uBtn(${i}, 'type', this.value)">
                    <option value="quick_reply" ${b.type==='quick_reply'?'selected':''}>Reply</option>
                    <option value="url" ${b.type==='url'?'selected':''}>URL</option>
                </select>
                <input type="text" value="${b.text}" placeholder="Button Label" oninput="uBtn(${i}, 'text', this.value)">
                <button class="remove-action" onclick="rBtn(${i})"><i class="fas fa-trash-alt"></i></button>
            </div>
            ${b.type === 'url' ? `
                <input type="text" value="${b.url || ''}" placeholder="https://example.com" oninput="uBtn(${i}, 'url', this.value)" style="margin-top:4px; font-size:0.8rem;">
            ` : ''}
        </div>
    `).join('');
    
    $('addBtn').style.display = buttons.length >= 3 ? 'none' : 'flex';
    updatePreview();
};

// Formatting Tools
window.format = (c) => {
    const el = $('bInput'), s = el.selectionStart, e = el.selectionEnd, v = el.value;
    el.value = v.substring(0, s) + c + v.substring(s, e) + c + v.substring(e);
    updatePreview();
    el.focus();
};

// Event Listeners
['hInput', 'bInput'].forEach(id => $(id).oninput = updatePreview);

$('addBtn').onclick = () => {
    if (buttons.length < 3) {
        buttons.push({ type: 'quick_reply', text: '' });
        renderBtnEditor();
    }
};

// Modal Logic
$('openAi').onclick = () => $('modal').classList.add('open');
window.closeModal = () => $('modal').classList.remove('open');

// AI API Integration
$('runAi').onclick = async () => {
    const p = $('aiPrompt').value;
    if(!p) return;
    
    const btn = $('runAi');
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';

    try {
        const res = await fetch('/generate_template', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ user_input: p, num_variations: 1 })
        });
        const [data] = await res.json();
        
        $('hInput').value = data.heading;
        $('bInput').value = data.body;
        buttons = data.buttons.map(b => ({...b, type: b.type.toLowerCase()}));
        
        renderBtnEditor();
        pollImg(data.image_path);
        closeModal();
    } catch (e) {
        alert("AI Service is temporarily unavailable.");
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
};

const pollImg = (url) => {
    $('dropText').innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Loading AI Image...';
    let attempts = 0;
    const timer = setInterval(() => {
        attempts++;
        const img = new Image();
        img.onload = () => {
            $('pImg').src = url;
            $('pImg').classList.remove('hidden');
            $('dropText').innerText = "Visual Ready";
            clearInterval(timer);
        };
        img.onerror = () => {
            if (attempts > 15) {
                $('dropText').innerText = "Failed to load image";
                clearInterval(timer);
            }
        };
        img.src = url + "?t=" + Date.now();
    }, 2000);
};

// Export & Utilities
$('copyT').onclick = () => {
    navigator.clipboard.writeText($('bInput').value);
    const btn = $('copyT');
    const old = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
    setTimeout(() => btn.innerHTML = old, 2000);
};

$('down').onclick = () => {
    const btn = $('down');
    btn.disabled = true;
    html2canvas($('capture'), { scale: 2, useCORS: true }).then(canvas => {
        const a = document.createElement('a');
        a.download = `wa-template-${Date.now()}.png`;
        a.href = canvas.toDataURL();
        a.click();
        btn.disabled = false;
    });
};

$('drop').onclick = () => $('imgUpload').click();
$('imgUpload').onchange = (e) => {
    const r = new FileReader();
    r.onload = (ev) => {
        $('pImg').src = ev.target.result;
        $('pImg').classList.remove('hidden');
        $('dropText').innerText = "Custom Image Loaded";
    };
    r.readAsDataURL(e.target.files[0]);
};

$('save').onclick = async () => {
    const btn = $('save');
    const old = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Saving...';
    
    try {
        await fetch('/submit_template', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                heading: $('hInput').value,
                body: $('bInput').value,
                image_prompt: "Manual",
                buttons: buttons
            })
        });
        alert("Template successfully saved and verified!");
    } catch (e) {
        alert("Save failed.");
    } finally {
        btn.innerHTML = old;
    }
};

// Init
updatePreview();
