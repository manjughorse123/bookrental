//Campus Bookstore Rentals

if( !!~window.location.href.indexOf("Receipt") || !!~window.location.href.indexOf("OrderSuccess")){
        window.AddShoppersConversion = {
                    order_id: document.querySelector("#autotest-orderid").innerText,
                    value: document.querySelector("tbody .os-totals+.os-totals td").innerText,
custom_fields: {
    currency: "",
    email: document.cookie.replace(/(?:(?:^|.*;\s*)cybbaEmailInput\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
    sessionid: document.cookie.replace(/(?:(?:^|.*;\s*)cybSessionID\s*\=\s*([^;]*).*$)|^.*$/, "$1")
}
        };
}
            var js = document.createElement('script'); js.type = 'text/javascript'; js.async = true; js.id = 'AddShoppers';
            js.src = ('https:' == document.location.protocol ? 'https://shop.pe/widget/' : 'http://cdn.shop.pe/widget/') + 'widget_async.js#5aaad627d5593032a26cf493';
            document.getElementsByTagName("head")[0].appendChild(js);