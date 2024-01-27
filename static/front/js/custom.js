function sweet_alert(text, icon) {
    Swal.fire({
        title: 'اعلان',
        text: text,
        icon: icon,
        showCancelButton: false,
        confirmButtonColor: '#3085d6',
        confirmButtonText: 'بستن'
    })
}

$(document).on('submit', '#article_comment', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/articles/add-article-comment',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            article_id: article_id,
            parent_id: $('#parent_id').val(),
            article_comment: $('#comment_text').val()
        },
        success: function (data) {
            console.log(data)
            $('#article_comment')[0].reset()
        }, error: function (data) {
            console.log('error')
        }
    })

})

function fillParentId(parentId) {
    $('#parent_id').val(parentId)
    document.getElementById('comment_form').scrollIntoView({behavior: "smooth"})
}

function filterProducts() {
    const filterPrice = $('#sl2').val()
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();
}

function fillPage(page) {
    $('#page').val(page)
    $('#filter_form').submit();
}

function showLargeImage(imageSrc) {
    $('#main_image').attr('src', imageSrc);
    $('#show_large_image_modal').attr('href', imageSrc);
}

function addProductToFavorite() {
    $.get('/products/product-favorite?product_id=' + productId).then(res => {
        console.log(res)
        if (res.status === 'success') {
            sweet_alert(res.text, 'success')
        } else if (res.status === 'exists') {
            sweet_alert(res.text, 'warning')
        } else if (res.status === 'not_found') {
            sweet_alert(res.text, 'error')
        } else if (res.status === 'not_auth') {
            Swal.fire({
                title: 'اعلان',
                text: res.text,
                icon: 'error',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                cancelButtonText: 'بستن',
                confirmButtonText: 'ورود به حساب کاربری'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/users/login';
                }
            })
        }
    })
}

function removeOrderDetail(detailId) {
    $.get('/users/remove-order-detail?detail_id=' + detailId).then(res => {
            if (res.status === 'success') {
                $('#order-detail-content').html(res.body);
            }
        }
    )
}

function changeOrderDetailCount(detailId, state) {
    $.get('/users/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
            if (res.status === 'success') {
                $('#order-detail-content').html(res.body);
            }
        }
    )
}

function addProductToBasket() {
    const productCount = $('#product-count').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
        if (res.status === 'success') {
            sweet_alert(res.text, 'success')
        } else if (res.status === 'exists') {
            sweet_alert(res.text, 'success')
        } else if (res.status === 'invalid_count') {
            sweet_alert(res.text, 'warning')
        } else if (res.status === 'not_found') {
            sweet_alert(res.text, 'error')
        } else if (res.status === 'not_auth') {
            Swal.fire({
                title: 'اعلان',
                text: res.text,
                icon: 'error',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                cancelButtonText: 'بستن',
                confirmButtonText: 'ورود به حساب کاربری'
            }).then((result) => {
                if (result.isConfirmed && res.status === 'not_auth') {
                    window.location.href = '/users/login';
                }
            })
        }
    })
}