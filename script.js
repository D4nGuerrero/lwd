// Replace this inferred address with the verified business inbox before launch.
const CONTACT_EMAIL = 'hello@laredowebdesigns.com';
document.querySelector('#copyright-year').textContent = String(new Date().getFullYear());

const testimonials = [
  { quote: '“LWD brought our vision to life. Our new website has made a huge difference!”', name: 'Marco G.', company: 'Border Brew Coffee' },
  { quote: '“Professional, creative, and easy to work with. Highly recommend the Laredo Web Designs team.”', name: 'Vanessa R.', company: 'Laredo Family Care' },
  { quote: '“They made the whole process simple and delivered a site we’re really proud of.”', name: 'Javier T.', company: 'Rivas Construction' },
  { quote: '“Our customers can finally find what they need, and the site feels like us.”', name: 'Elena M.', company: 'South Texas Market' },
  { quote: '“The team listened closely and stayed with us well beyond launch.”', name: 'Daniel C.', company: 'Laredo Community Studio' },
];

const projects = {
  coffee: { title: 'Border Brew Coffee', image: 'assets/work-border-brew.jpg', copy: 'A warm, memorable online home for a local coffee shop, with visual branding and search-friendly content.' },
  rivas: { title: 'Rivas Construction', image: 'assets/work-rivas.jpg', copy: 'A confident portfolio and clear service pages that help customers see the strength of a Laredo construction team.' },
  care: { title: 'Laredo Family Care', image: 'assets/work-family-care.jpg', copy: 'An inviting, easy-to-use site designed to help families connect with care close to home.' },
};

let firstTestimonial = 0;
const testimonialList = document.querySelector('.testimonial-cards');

function renderTestimonials() {
  testimonialList.replaceChildren();
  for (let offset = 0; offset < 3; offset += 1) {
    const item = testimonials[(firstTestimonial + offset) % testimonials.length];
    const card = document.createElement('article');
    card.className = 'testimonial-card';
    const quote = document.createElement('blockquote');
    quote.textContent = item.quote;
    const stars = document.createElement('span');
    stars.className = 'stars';
    stars.setAttribute('aria-label', 'Five out of five stars');
    stars.textContent = '★★★★★';
    const person = document.createElement('p');
    person.className = 'person';
    person.textContent = item.name;
    const company = document.createElement('p');
    company.className = 'company';
    company.textContent = item.company;
    card.append(quote, stars, person, company);
    testimonialList.append(card);
  }
}
renderTestimonials();

document.querySelector('.carousel-arrow.previous').addEventListener('click', () => {
  firstTestimonial = (firstTestimonial - 1 + testimonials.length) % testimonials.length;
  renderTestimonials();
});
document.querySelector('.carousel-arrow.next').addEventListener('click', () => {
  firstTestimonial = (firstTestimonial + 1) % testimonials.length;
  renderTestimonials();
});

const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.primary-nav');
menuButton.addEventListener('click', () => {
  const open = nav.classList.toggle('is-open');
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  nav.classList.remove('is-open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open menu');
}));

const quoteDialog = document.querySelector('#quote-dialog');
const projectDialog = document.querySelector('#project-dialog');
document.querySelectorAll('[data-quote]').forEach(button => button.addEventListener('click', () => {
  if (projectDialog.open) projectDialog.close();
  quoteDialog.showModal();
}));
document.querySelectorAll('[data-project]').forEach(button => button.addEventListener('click', () => {
  const project = projects[button.dataset.project];
  document.querySelector('#project-dialog-image').src = project.image;
  document.querySelector('#project-dialog-image').alt = `${project.title} website preview`;
  document.querySelector('#project-dialog-title').textContent = project.title;
  document.querySelector('#project-dialog-copy').textContent = project.copy;
  projectDialog.showModal();
}));
document.querySelectorAll('[data-close]').forEach(button => button.addEventListener('click', () => button.closest('dialog').close()));
document.querySelectorAll('dialog').forEach(dialog => dialog.addEventListener('click', event => {
  if (event.target === dialog) dialog.close();
}));

document.querySelector('#quote-form').addEventListener('submit', event => {
  event.preventDefault();
  const values = new FormData(event.currentTarget);
  const subject = encodeURIComponent(`Website inquiry from ${values.get('name')}`);
  const body = encodeURIComponent(`Name: ${values.get('name')}\nEmail: ${values.get('email')}\nService: ${values.get('service')}\n\nProject details:\n${values.get('details')}`);
  window.location.href = `mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}`;
});
