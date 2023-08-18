function saveOptions(e) {
  var api_key = document.querySelector("#api_key").value
  chrome.storage.local.set({"api_key": api_key}).then(restoreOptions)  
  e.preventDefault();
}

function restoreOptions() {
  chrome.storage.local.get("api_key").then(function(data) {
    if (typeof data['api_key'] != 'undefined') {
      var api_key = data['api_key']
      document.querySelector("#api_key").value = api_key
    }
  })

}

document.addEventListener('DOMContentLoaded', restoreOptions)
document.querySelector("form").addEventListener("submit", saveOptions)