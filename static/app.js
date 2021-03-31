downloadLink.addEventListener('click', (e) => {
  let folderName = window.location.pathname.substring(10, window.location.pathname.length);

  // Make the request to delete the folder once the file has been downloaded.
  fetch(`/backup/${folderName}`, {
    method: 'DELETE'
  // If the process went successfully, redirect the user back to the home page.
  }).then(response => {
    window.location.href = '/'
  })
})
