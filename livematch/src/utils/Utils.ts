import jQuery from 'jquery';

export function initJQueryCSRF(): void {
    jQuery.ajaxSetup({
        beforeSend: (xhr: JQueryXHR) => {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
    });
}


export function getCookie(name: string): string {
    let cookieValue: string = null;
    if (document.cookie != null && document.cookie !== '') {
        let cookies: string[] = document.cookie.split(';');
        for (let cookieRaw of cookies) {
            let cookie: string = jQuery.trim(cookieRaw);
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
