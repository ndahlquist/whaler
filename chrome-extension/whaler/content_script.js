/**
 * Our CSS colors the merge buttons blue.
 */
function injectCSS() {
  var link = document.createElement('link');
  link.href = chrome.extension.getURL('css/whaler.css');
  link.rel = 'stylesheet';
  head = document.getElementsByTagName ("head")[0] || document.documentElement;
  head.insertBefore(link, head.lastChild);
}

function modifyMergeButton() {
  button = document.querySelector(".merge-branch-action");
  // Add our CSS tag to paint the button blue.
  button.className = button.className.replace(/primary/g, 'whaler');
  button.onclick = modifyMergeForm
}

function modifyMergeForm() {
  form = document.querySelector(".merge-branch-form");
  // Redirect the form to our server, so that we can handle the merge.
  form.action = "https://whaler-on-fleek.appspot.com/queue_merge";

  confirmMergeButton = form.querySelector(".button");
  // Add our CSS tag to paint the button blue.
  confirmMergeButton.className = confirmMergeButton.className.replace(/primary/g, 'whaler');
}

injectCSS();
modifyMergeButton();
modifyMergeForm();

