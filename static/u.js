function u_getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}
function u__ajax(_url, isAsync, successFunction, isGet) {
    if (isGet)
        $.ajax({
            url: _url,
            async: isAsync,

            success: function (msg) {
                successFunction(msg)
            },
            dataType: "text",
            error: function () {
                console.log('ajax failure: ' + _url);
            }
        });
    else {
        $.ajax({
            url: _url,
            async: isAsync,

            success: function (msg) {
                successFunction(msg)
            },
            dataType: "text",
            error: function () {
                console.log('ajax failure: ' + _url);
            }
        });
    }
}

function u_ajax(_url, isAsync, successFunction) {
    u__ajax(_url, isAsync, successFunction, true)
}

function u_postAjax(_url, isAsync, successFunction) {
    u__ajax(_url, isAsync, successFunction, false)
}

function u_syncAjax(url) {
    var result;
    u_ajax(url, false, function (m) {
        result = m
    });
    return result
}

function u_getAjaxObject(url) {
    return JSON.parse(u_syncAjax(url))
}

function u_asyncAjax(url, successFunction) {
    u_ajax(url, true, successFunction)
}

function u_inform(str) {
    var $copysuc = $("<div id='spec1a1forInform' style='font-size:20px;position:fixed;z-index:999;bottom:50%;left:50%;" +
    "margin:0 0 -20px -80px;background-color:rgba(0, 0, 0, 0.2);" +
    "filter:progid:DXImageTransform.Microsoft.Gradient(startColorstr=#30000000, endColorstr=#30000000);" +
    "padding:6px;'><div style='padding:10px 20px;text-align:center;border:1px solid #F4D9A6;" +
    "background-color:#FFFDEE;'>" + str + "</div></div>");
    $("body").find("#spec1a1forInform").remove().end().append($copysuc);
    $("#spec1a1forInform").fadeOut(3000);
}

//��URL�е�UTF-8�ַ���ת�������ַ���
function u_utf82Chinese(str) {

    //������ת�����ַ�
    function utf8ToChar(str) {
        var iCode, iCode1, iCode2;
        iCode = parseInt("0x" + str.substr(1, 2));
        iCode1 = parseInt("0x" + str.substr(4, 2));
        iCode2 = parseInt("0x" + str.substr(7, 2));
        return String.fromCharCode(((iCode & 0x0F) << 12) | ((iCode1 & 0x3F) << 6) | (iCode2 & 0x3F));
    }

    var cstr = "";
    var nOffset = 0;
    if (str == "")
        return "";
    str = str.toLowerCase();
    nOffset = str.indexOf("%e");
    if (nOffset == -1)
        return str;
    while (nOffset != -1) {
        cstr += str.substr(0, nOffset);
        str = str.substr(nOffset, str.length - nOffset);
        if (str == "" || str.length < 9)
            return cstr;
        cstr += utf8ToChar(str.substr(0, 9));
        str = str.substr(9, str.length - 9);
        nOffset = str.indexOf("%e");
    }
    return cstr + str;
}

function u_saveFile(str, path) {
    str = u_reformatUrlParameter(str);
    u_ajax('saveFile?path=' + path + "&content=" + str, true, function (msg) {
        u_inform(1)
    });
}

function u_reformatUrlParameter(mstring) {
    var i = 0;
    var n = 0;
    var c = "";
    var s = "";
    for (i = 0; i < mstring.length; i++) {
        c = mstring.charAt(i);
        n = mstring.charCodeAt(i);
        if (n == 13) {
            c = "%0D";
        }
        if (n == 10) {
            c = "%0A";
        }
        if (n == 38) {
            c = "%26";
        }
        if (n == 35) {  //#
            c = "%23";
        }
        if (n == 43) {  //#
            c = "%2B";
        }
        s = s + c;
    }
    return s;
}

function u_strStartsWith(str, startStr) {
    if (str.length < startStr.length || str.substring(0, startStr.length) != startStr)
        return false;
    return true;
}

function u_strEndsWith(str, endStr) {
    if (str.length < endStr.length || str.substring(str.length - endStr.length, str.length) != endStr)
        return false;
    return true;
}

function u_clueTip(jqueryObj, text) {
    jqueryObj.css({
        'text-decoration': 'underline',
        'cursor': 'pointer'
    });
    var boxId = (Math.random() + "").substr(2);
    $('body').append('<div id="' + boxId + '" style="display:none;position:absolute;padding:10px 14px; ' +
    'background:#fff; border:1px solid #bebebe;">' + text + '</div>');
    var d = $('#' + boxId);
    var pos = jqueryObj.offset();
    d.css({"top": pos.top + jqueryObj.height(), "left": pos.left + jqueryObj.width() / 2});
    jqueryObj.click(function () {
        if (d.css('display') == 'none')
            d.show();
        else
            d.hide()
    });
}

function u_clueHtml(jqueryObj, htmlPath) {
    u_clueTip(jqueryObj, u_syncAjax('getFileStr?path=' + htmlPath))
}

function u_getFileStr(path) {
    return u_syncAjax('getFileStr?path=' + path);
}

function u_loadMathjax(){//不起作用，why？
    $('head').append(u_getFileStr('static/reuse/mathjax.html'))
}

////////////// health robot
function u_inArray(s, ar){
	for(var i in ar)
		if (ar[i]==s)
			return true;
	return false;
}