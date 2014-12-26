function queueMerge() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "https://whaler-on-fleek.appspot.com/queue_merge", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.setRequestHeader("Access-Control-Request-Headers", "Access-Control-Allow-Origin");
    xmlhttp.send();
}

function crippleMergeButton(element) {
    if (element.className.indexOf("primary") > -1) {
      element.className = element.className.replace(/primary/g, 'whaler').replace(/js-details-target/g, '');
      element.onclick=function(){
        element.className = element.className.replace(/whaler/g, 'disabled');
        queueMerge();
      };
    }
}

window.onload = function() {
  crippleMergeButton(document.querySelector(".merge-branch-action"));
}

var link = document.createElement('link');
link.href = chrome.extension.getURL('css/whaler.css');
link.rel = 'stylesheet';
head = document.getElementsByTagName ("head")[0] || document.documentElement;
head.insertBefore(link, head.lastChild);
