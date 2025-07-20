function toggleDark() {
    var checkbox = document.getElementById('dark-mode');
    var r = document.querySelector(':root');
    if (checkbox.checked == true) {
        r.style.setProperty('--main-bg', '#212121');
        r.style.setProperty('--line', '#454545');
        r.style.setProperty('--nav-link-active', '#3A3A3A');
        r.style.setProperty('--nav-link-hover', '#2C2C2C');
        r.style.setProperty('--nav-link-icon', '#d1d1d1');
        r.style.setProperty('--text', '#fff');
        r.style.setProperty('--main-red', '#F92B67');
        r.style.setProperty('--hover-red', '#e12b5f');
        r.style.setProperty('--second-text', '#C0C0C0');
    }
    else {
        r.style.setProperty('--main-bg', '#fff');
        r.style.setProperty('--line', '#d1d1d1');
        r.style.setProperty('--nav-link-active', '#ffebf2');
        r.style.setProperty('--nav-link-hover', '#FAF4F6');
        r.style.setProperty('--nav-link-icon', '#555555');
        r.style.setProperty('--text', '#212121');
        r.style.setProperty('--main-red', '#F92B67');
        r.style.setProperty('--hover-red', '#e12b5f');
        r.style.setProperty('--second-text', '#a0a0a0');
    }
}