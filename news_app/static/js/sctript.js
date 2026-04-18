document.addEventListener("DOMContentLoaded", function () {
    console.log("Blog Tin Tuc da san sang.");
});

//THEME TOGGLE (sáng / tối)
const html = document.documentElement;
const toggleBtn = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);

    if (theme === 'dark') {
        themeIcon.className = 'bi bi-sun-fill';
    } else {
        themeIcon.className = 'bi bi-moon-fill';
    }
}

//Khôi phục theme đã lưu khi load trang
const savedTheme = localStorage.getItem('theme') || 'light';
applyTheme(savedTheme);

//Nhấn nút toggle
toggleBtn.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    applyTheme(current === 'dark' ? 'light' : 'dark');
});

//BÌNH LUẬN INLINE
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        for (let cookie of document.cookie.split(';')) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function batDauSua(id) {
    document.querySelector(`.comment-text-${id}`).classList.add('d-none');
    document.querySelector(`.comment-input-${id}`).classList.remove('d-none');

    const box = document.querySelector(`#comment-${id}`);
    box.querySelector('[onclick^="batDauSua"]').classList.add('d-none');
    box.querySelector('[onclick^="luuBinhLuan"]').classList.remove('d-none');
    box.querySelector('[onclick^="huyBinhLuan"]').classList.remove('d-none');
}

function huyBinhLuan(id) {
    document.querySelector(`.comment-text-${id}`).classList.remove('d-none');
    document.querySelector(`.comment-input-${id}`).classList.add('d-none');

    const box = document.querySelector(`#comment-${id}`);
    box.querySelector('[onclick^="batDauSua"]').classList.remove('d-none');
    box.querySelector('[onclick^="luuBinhLuan"]').classList.add('d-none');
    box.querySelector('[onclick^="huyBinhLuan"]').classList.add('d-none');
}

async function luuBinhLuan(id, url) {
    const noiDung = document.querySelector(`.comment-input-${id}`).value.trim();

    if (!noiDung) {
        alert('Nội dung không được trống!');
        return;
    }

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ noi_dung: noiDung }),
    });

    const data = await response.json();

    if (data.success) {
        document.querySelector(`.comment-text-${id}`).innerText = data.noi_dung;
        huyBinhLuan(id);
    } else {
        alert(data.error || 'Có lỗi xảy ra.');
    }
}

