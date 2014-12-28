var BASE_URL = "https://dev-dot-whaler-on-fleek.appspot.com" // TODO

/**
 * Our CSS makes the merge buttons blue.
 */
function injectCSS() {
  var link = document.createElement('link');
  link.href = chrome.extension.getURL('css/whaler.css');
  link.rel = 'stylesheet';
  head = document.getElementsByTagName ('head')[0] || document.documentElement;
  head.insertBefore(link, head.lastChild);
}

function updateDocument() {
  if (!/\/pull\//.test(document.URL)) {
    // This is not a pull request URL.
    return false;
  }
  mergeButton = document.querySelector('.merge-branch-action');
  if (mergeButton != null) {
    // Add our CSS tag to paint the button blue.
    mergeButton.className = mergeButton.className.replace(/primary/g, 'whaler');
    // Modify the text
    mergeButton.innerHTML = mergeButton.innerHTML.replace(/Merge pull request/g, 'Squash merge')

    mergeButton.addEventListener("click", requestOauth)
  }

  form = document.querySelector('.merge-branch-form');
  if (form != null) {

    // Redirect the form to our server so that we can handle the merge.
    form.action = BASE_URL + '/queue_merge';

    // We don't need this field, so we replace it with username.
    auth_token_field = form.querySelector('input[name="authenticity_token"]');
    if (auth_token_field != null) {
      auth_token_field.name = 'username'
      auth_token_field.value = getUsername()
    }

    confirmMergeButton = form.querySelector('.button');
    // Add our CSS tag to paint the button blue.
    confirmMergeButton.className = confirmMergeButton.className.replace(/primary/g, 'whaler');
  }
}

function getUsername() {
  name_header = document.querySelector('a.header-nav-link.name')
  return name_header.href.replace(/https:\/\/github.com\// ,'')
}

var has_oauth = true

function checkOauth() {
  url = BASE_URL + '/has_oauth?username=' + getUsername()
  $.get(url, function(responseText) {
    if (responseText !== 'true') has_oauth = false
  });
}

function requestOauth() {
  if (has_oauth) return;
  window.location.href = "https://github.com/login/oauth/authorize?" +
                         "client_id=331e31888360cb8fff32&" +
                         "redirect_uri=" + BASE_URL + "/oauth_callback/" + getUsername() +
                         "&scope=public_repo,repo,write:repo_hook" +
                         "&state=" + document.URL;
}

function domNodeInsertedCallback() {
    // We must remove the event listener before updateDocument() to prevent recursion.
    document.removeEventListener('DOMNodeInserted', domNodeInsertedCallback);
    updateDocument();
    document.addEventListener('DOMNodeInserted', domNodeInsertedCallback);
}

injectCSS();
updateDocument();
checkOauth();

// GitHub dynamically modifies the merge form. We need to make sure we apply our modifications when it is updated.
// TODO: This is allegedly terrible for performance. What's a better way of doing this?
document.addEventListener('DOMNodeInserted', domNodeInsertedCallback);

