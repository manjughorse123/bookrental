function isMobile() {
    return screen.width <= 435;   //375 iPhone 6 width, 414 = iPhone 6 Plus, 435 Nexus 6P
}

function isTablet() {
    return screen.width <= 768 && screen.width > 435;
}

function isDesktop() {
    return screen.width > 768;
}

function supportsType(inputType) {
    var input = document.createElement('input');
    input.type = inputType;
    var desiredType = input.getAttribute('type');
    var supported = false;
    if (input.type === desiredType) {
        supported = true;
    }
    input.value = 'Hello world';
    var helloWorldAccepted = (input.value === 'Hello world');
    switch (desiredType) {
        case "email":
        case "url":
            if (!input.validationMessage) {
                supported = false;
            }
            break;
        case "color":
        case "date":
        case "datetime":
        case "month":
        case "number":
        case "time":
        case "week":
            if (helloWorldAccepted) {
                supported = false;
            }
            break;
    }
    return supported;
}

function isElementInViewport(el) {
    var rect = el[0].getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= $(window).height() &&
        rect.right <= $(window).width()
    );
}