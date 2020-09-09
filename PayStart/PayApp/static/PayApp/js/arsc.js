window.onload = function() {
  document.getElementsByClassName("loader_div")[0].style.top = "-200%";
  document.getElementsByClassName("loader_div")[0].style.display = "none";
  document.body.style.overflow = "scroll";
};

const intro = document.getElementsByClassName("landing-sec")[0];
const inner_sec = document.getElementsByClassName("inner-section")[0];
const logo = document.getElementsByClassName("logo")[0];
const op_div = document.getElementsByClassName("op_div")[0];
const end = document.getElementsByClassName("about-div")[0];
const reg_div = document.getElementsByClassName("reg_button_div")[0];
const reg_button = document.getElementsByClassName("reg_button")[0];

const mob_intro = document.getElementsByClassName("mob_landing")[0];
const mob_inner_sec = document.getElementsByClassName("mob_inner-section")[0];
const mob_logo = document.getElementsByClassName("mob_logo")[0];
const mob_op_div = document.getElementsByClassName("mob_op_div")[0];
const controller = new ScrollMagic.Controller();

const textAnim = TweenMax.fromTo(
  inner_sec,
  1,
  { width: "98%", height: "95%" },
  { width: "100%", height: "100%" }
);

// const mobtextAnim = TweenMax.fromTo(
//   mob_inner_sec,
//   1,
//   { width: "90%", height: "93%" },
//   { width: "100%", height: "100%" }
// );

// let scene4 = new ScrollMagic.Scene({
//   duration: 500,
//   triggerElement: mob_intro,
//   triggerHook: 0
// })
//   .setTween(mobtextAnim)
//   .setPin(mob_intro)
//   .addTo(controller);

// const moblogoAnim = TweenMax.fromTo(
//   mob_logo,
//   0.5,
//   { opacity: 1 },
//   { opacity: 0 }
// );

// let scene5 = new ScrollMagic.Scene({
//   duration: 500,
//   triggerElement: mob_intro,
//   triggerHook: 0
// })
//   .setTween(moblogoAnim)
//   .addTo(controller);

// const mob_op_divanim = TweenMax.fromTo(
//   mob_op_div,
//   0.2,
//   { opacity: 1 },
//   { opacity: 0 }
// );

// let scene6 = new ScrollMagic.Scene({
//   duration: 200,
//   triggerElement: mob_intro,
//   triggerHook: 0
// })
//   .setTween(mob_op_divanim)
//   .addTo(controller);

let scene2 = new ScrollMagic.Scene({
  duration: 500,
  triggerElement: intro,
  triggerHook: 0
})
  .setTween(textAnim)
  .setPin(intro)
  .addTo(controller);

const logoAnim = TweenMax.fromTo(logo, 0.5, { opacity: 1 }, { opacity: 0 });

let scene = new ScrollMagic.Scene({
  duration: 500,
  triggerElement: intro,
  triggerHook: 0
})
  .setTween(logoAnim)
  .addTo(controller);

const op_divanim = TweenMax.fromTo(op_div, 0.2, { opacity: 1 }, { opacity: 0 });

let scene3 = new ScrollMagic.Scene({
  duration: 200,
  triggerElement: intro,
  triggerHook: 0
})
  .setTween(op_divanim)
  .addTo(controller);

const reg_divanim = TweenMax.fromTo(
  reg_div,
  0.5,
  { opacity: 1 },
  { opacity: 0 }
);

let scene4 = new ScrollMagic.Scene({
  duration: 200,
  triggerElement: intro,
  triggerHook: 0
})
  .setTween(reg_divanim)
  .addTo(controller);

if (window.screen.width < 900) {
  document.getElementsByClassName("about-div")[0].style.flexDirection =
    "column-reverse";
  document.getElementsByClassName("text")[1].style.border = "0px 0px 0px 0px";
  document.getElementsByClassName("text")[0].removeAttribute("data-aos");
} else if (window.screen.width > 800) {
  document.getElementsByClassName("text")[1].style.borderRadius =
    "102px 0px 0px 102px";
  console.log(document.getElementsByClassName("text"));
}

document.getElementsByClassName("reg_button_div")[0].onclick = function() {
  window.location.href = "./registration.html";
};

document.getElementsByClassName("mob_reg_button_div")[0].onclick = function() {
  window.location.href = "./registration.html";
};
