const items = document.querySelectorAll(".item");
const items2 = document.querySelectorAll(".item2");
const previa = document.getElementById("previa");
const previa2 = document.getElementById("previa2")

items.forEach(e => {
  e.addEventListener("mouseenter", () => {
    const atributo = e.getAttribute("data-img");

    // Faz a imagem sumir
    previa.style.opacity = 0;

    // Espera a animação de sumir terminar, troca a imagem e reaparece
    setTimeout(() => {
      previa.src = atributo;
      previa.style.opacity = 1;
    }, 100); // tempo igual ao do CSS transition
  });
});

items2.forEach(e => {
  e.addEventListener("mouseenter", () => {
    const atributo = e.getAttribute("data-img");

    // Faz a imagem sumir
    previa2.style.opacity = 0;

    // Espera a animação de sumir terminar, troca a imagem e reaparece
    setTimeout(() => {
      previa2.src = atributo;
      previa2.style.opacity = 1;
    }, 100); // tempo igual ao do CSS transition
  });
});