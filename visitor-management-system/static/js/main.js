
/*$(document).ready(function () {
    if ($('#visitorTable').length) {
        $('#visitorTable').DataTable();
    }
});

function confirmDelete(entity, url) {
    if (confirm(`Are you sure you want to delete this ${entity}?`)) {
        window.location.href = url;
    }
}
*/

$(document).ready(function () {
    if ($('#visitorTable').length) {
        $('#visitorTable').DataTable();
    }

    
    const hamburgerBtn = $('.hamburger-menu');
    const closeBtn = $('.close-menu');
    const mobileMenu = $('#mobile-menu');

    
    hamburgerBtn.on('click', function() {
        mobileMenu.addClass('active');
        $('body').css('overflow-y', 'hidden'); 
    });

    
    closeBtn.on('click', function() {
        mobileMenu.removeClass('active');
        $('body').css('overflow-y', 'auto'); 
    });

    
    mobileMenu.find('a').on('click', function() {
        mobileMenu.removeClass('active');
        $('body').css('overflow-y', 'auto');
    });

});

function confirmDelete(entity, url) {
 
    showCustomConfirm(`Are you sure you want to delete this ${entity}?`, function() {
        window.location.href = url;
    });
}


function showCustomConfirm(message, callback) {
    
    const modalHtml = `
        <div id="customConfirmModal" style="
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6); display: flex; justify-content: center;
            align-items: center; z-index: 2000;
        ">
            <div style="
                background: white; padding: 30px; border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3); max-width: 400px;
                text-align: center;
            ">
                <p style="font-size: 1.1em; margin-bottom: 20px;">${message}</p>
                <button id="confirmYes" style="
                    background: #2575fc; color: white; padding: 10px 20px;
                    border: none; border-radius: 5px; cursor: pointer; margin-right: 10px;
                ">Yes</button>
                <button id="confirmNo" style="
                    background: #ccc; color: #333; padding: 10px 20px;
                    border: none; border-radius: 5px; cursor: pointer;
                ">No</button>
            </div>
        </div>
    `;

    $('body').append(modalHtml);

    $('#confirmYes').on('click', function() {
        $('#customConfirmModal').remove();
        if (callback) callback();
    });

    $('#confirmNo').on('click', function() {
        $('#customConfirmModal').remove();
    });
}