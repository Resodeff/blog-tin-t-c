document.addEventListener("DOMContentLoaded", function() {
    console.log("Hệ thống ZERO AI đã tải xong!");

    const nutMuaHang = document.querySelectorAll('.btn-primary');

    nutMuaHang.forEach(function(nut) {
        nut.addEventListener('click', function(su_kien) {
            su_kien.preventDefault(); 
            alert("Cảm ơn bạn! Giám đốc đang xây dựng tính năng Giỏ hàng. Vui lòng quay lại sau nhé!");
        });
    });
});