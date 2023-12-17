$(document).ready(function () {
    
    // Vertical align login and signup forms
    $(window).resize(containerMargin)

    function containerMargin() {
        let netHeight = window.innerHeight - $('header').height();
        let margin = (netHeight - $('#main').height()) / 2;
        $('#main').css('margin-top', margin)
    }

    containerMargin();

    // Dashboard sidebar dropdowns
    $('.sidebar .dropdown').on('show.bs.dropdown', function () {
        let i = $(this).find(".fas");
        i.removeClass('fa-angle-right');
        i.addClass('fa-angle-down');
        console.log($(this).find('.dropdown-menu'))
        $(this).find('.dropdown-menu').first().stop(true,true).slideDown(250);
    });

    $('.sidebar .dropdown').on('hide.bs.dropdown', function () {
        let i = $(this).find(".fas");
        i.removeClass('fa-angle-down');
        i.addClass('fa-angle-right');
        $(this).find('.dropdown-menu').first().stop(true,true).slideUp(200);
    });

    // Dashboard header collapse 
    $('#navbarCollapse').on('shown.bs.collapse', pushContainer);
    $('#navbarCollapse').on('hidden.bs.collapse', pushContainer);

    function pushContainer() {
        let height = $('header').height();
        $('.container-fluid').css('margin-top', height - 55 + "px");
        $('.sidebar').css('top', height);
    }

    // Page subtitle align
    let lineHeight = $('.page-subtitle').parent().height();
    $('.page-subtitle').css('line-height',lineHeight + 'px');
    
    // Additional table data
    // Operation column for data table
    let tableHeadHtml = '<th>Operation</th>';
    $('#data-table thead th').last().after(tableHeadHtml)

    // Operation column content, edit and delete buttons
    let tableDataHtml = '<td><a href="edit.html" class="btn btn-sm btn-primary">Edit</a> <a href="" class="btn btn-sm btn-danger">Delete</a></td>';
    $('tbody tr').append(tableDataHtml);

    // Data Table initializer
    $(document).ready(function () {
        $('#data-table').DataTable();
    });
})
