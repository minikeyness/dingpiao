/**
 * Created by whz on 2015-12-23.
 * ajax提交表单是添加csrftoken,使其通过验证
 */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
$.blockUI.defaults.css={};//中间内容的css
$.blockUI.defaults.css= {
    padding:        0,
    margin:         0,
    width:          '30%',
    top:            '40%',
    left:           '35%',
    textAlign:      'center',
    color:          '#fff',
    border:         '1px solid #aaa',
    backgroundColor:'#000',
    cursor:         'point',
    '-webkit-border-radius': '10px',
    '-moz-border-radius': '10px',
    'border-radius': '10px',
    opacity: .9,//基本不透明
};
$.blockUI.defaults.message=null;
$.blockUI.defaults.message='<h2>请稍等...</h2>';
$.blockUI.defaults.overlayCSS.cursor='point';
$.blockUI.defaults.overlayCSS.opacity=0.5;//覆盖层的透明度
$(document).ajaxStart($.blockUI).ajaxStop($.unblockUI);

//blockUI扩展
myalert=function(msg){
    $.blockUI({
        message:'<h2>'+msg+'</h2><br/><input class="btn btn-primary" type="button" value="确认" onclick="$.unblockUI()">',
    overlayCSS: { backgroundColor: '#000',opacity:0.2}
    });
}