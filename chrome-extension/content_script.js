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
  if (button == null) return;
  // Add our CSS tag to paint the button blue.
  button.className = button.className.replace(/primary/g, 'whaler');
  button.onclick = modifyMergeForm
}

function modifyMergeForm() {
  form = document.querySelector(".merge-branch-form");
  if (form == null) return;
  // Redirect the form to our server, so that we can handle the merge.
  form.action = "https://whaler-on-fleek.appspot.com/queue_merge";

  confirmMergeButton = form.querySelector(".button");
  // Add our CSS tag to paint the button blue.
  confirmMergeButton.className = confirmMergeButton.className.replace(/primary/g, 'whaler');
}

injectCSS();

modifyMergeButton();
modifyMergeForm();

// GitHub dynamically modifies the merge form. We need to make sure we apply our modifications when it is updated.
// TODO: This is allegedly terrible for performance. What's a better way of doing this?
document.addEventListener('DOMNodeInserted', function() {
    console.log('DOMNodeInserted event.');
    modifyMergeButton();
    modifyMergeForm();
}, true);

