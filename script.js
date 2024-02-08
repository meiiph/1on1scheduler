const openPopupButton = document.getElementById('openPopup');
const closePopupButton = document.getElementById('closePopup');
const popup = document.getElementById('popup');

openPopupButton.addEventListener('click', () => {
  popup.style.display = 'block';
});

closePopupButton.addEventListener('click', () => {
  popup.style.display = 'none';
});
