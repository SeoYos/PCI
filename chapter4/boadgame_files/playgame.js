function MM_preloadImages() { //v3.0
  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
    var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
    if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}
function preloadimg() {
	MM_preloadImages("http://www.gamers-jp.com/playgame/images/index_11.gif","http://www.gamers-jp.com/playgame/images/index_03.gif");
	MM_preloadImages("http://www.gamers-jp.com/playgame/images/homebtn.gif","http://www.gamers-jp.com/playgame/images/homebtn_ov.gif");
	MM_preloadImages("http://www.gamers-jp.com/playgame/images/gamebtn.gif","http://www.gamers-jp.com/playgame/images/gamebtn_ov.gif");
	MM_preloadImages("http://www.gamers-jp.com/playgame/images/textbtn.gif","http://www.gamers-jp.com/playgame/images/textbtn_ov.gif");
	MM_preloadImages("http://www.gamers-jp.com/playgame/images/linkbtn.gif","http://www.gamers-jp.com/playgame/images/linkbtn_ov.gif");
	MM_preloadImages("http://www.gamers-jp.com/playgame/images/bbsbtn.gif","http://www.gamers-jp.com/playgame/images/bbsbtn_ov.gif");
	MM_preloadImages("http://www.gamers-jp.com/playgame/images/aboutbtn.gif","http://www.gamers-jp.com/playgame/images/aboutbtn_ov.gif");
}

function myGo(){
  mySelect = document.myForm.myMenu.selectedIndex;
  location.href = document.myForm.myMenu.options[mySelect].value;
}

// Copyright (c) 1996-1997 Athenia Associates.
// http://www.webreference.com/js/
// License is granted if and only if this entire
// copyright notice is included. By Tomer Shiran.

function setCookie (name, value, expires, path, domain, secure) {
    var curCookie = name + "=" + escape(value) + (expires ? "; expires=" + expires : "") +
        (path ? "; path=" + path : "") + (domain ? "; domain=" + domain : "") + (secure ? "secure" : "");
    document.cookie = curCookie;
}

function getCookie (name) {
    var prefix = name + '=';
    var c = document.cookie;
    var nullstring = '';
    var cookieStartIndex = c.indexOf(prefix);
    if (cookieStartIndex == -1)
        return nullstring;
    var cookieEndIndex = c.indexOf(";", cookieStartIndex + prefix.length);
    if (cookieEndIndex == -1)
        cookieEndIndex = c.length;
    return unescape(c.substring(cookieStartIndex + prefix.length, cookieEndIndex));
}

function deleteCookie (name, path, domain) {
    if (getCookie(name))
        document.cookie = name + "=" + ((path) ? "; path=" + path : "") +
            ((domain) ? "; domain=" + domain : "") + "; expires=Thu, 01-Jan-70 00:00:01 GMT";
}

function fixDate (date) {
    var base = new Date(0);
    var skew = base.getTime();
    if (skew > 0)
        date.setTime(date.getTime() - skew);
}