// Supported languages: 'es' (default) | 'en'
// Usage:  t('key')  → returns translated string for the active language.
// Call    applyLanguage()  on DOMContentLoaded (already done automatically)

const TRANSLATIONS = {

  // ── Top bar / Settings panel ──────────────────────────────────────────────
  'settings.title':            { es: 'Ajustes',              en: 'Settings' },
  'settings.account':          { es: 'Cuenta',               en: 'Account' },
  'settings.viewProfile':      { es: 'Ver mi perfil',        en: 'View my profile' },
  'settings.editProfile':      { es: 'Editar perfil',        en: 'Edit profile' },
  'settings.subscription':     { es: 'Suscripción',          en: 'Subscription' },
  'settings.goPremium':        { es: 'Hazte Premium',        en: 'Go Premium' },
  'settings.goPremiumSub':     { es: 'Temas, cupones y receta exclusiva', en: 'Themes, coupons & exclusive recipe' },
  'settings.premiumActive':    { es: 'Plan Premium activo',  en: 'Premium plan active' },
  'settings.changePayment':    { es: 'Cambiar método de pago', en: 'Change payment method' },
  'settings.cancelSub':        { es: 'Cancelar suscripción', en: 'Cancel subscription' },
  'settings.appearance':       { es: 'Apariencia',           en: 'Appearance' },
  'settings.colorTheme':       { es: 'Tema de color',        en: 'Color theme' },
  'settings.language':         { es: 'Idioma',               en: 'Language' },
  'settings.logout':           { es: 'Cerrar sesión',        en: 'Log out' },
  'settings.themeOrange':      { es: 'Naranja',              en: 'Orange' },
  'settings.themeGreen':       { es: 'Verde',                en: 'Green' },
  'settings.themeDark':        { es: 'Oscuro',               en: 'Dark' },

  // ── Premium panel ─────────────────────────────────────────────────────────
  'premium.zone':              { es: '✨ Zona Premium',      en: '✨ Premium Zone' },
  'premium.weeklyRecipe':      { es: 'Receta de la semana',  en: 'Recipe of the week' },
  'premium.weeklyLabel':       { es: 'Esta semana',          en: 'This week' },
  'premium.weeklyBy':          { es: 'Por el equipo Trastevere 🍅', en: 'By the Trastevere team 🍅' },
  'premium.coupon1':           { es: '10% Mercadona',             en: '10% Mercadona' },
  'premium.coupon2':           { es: '5€ El Corte Inglés',        en: '5€ El Corte Inglés' },
  'premium.coupon3':           { es: 'Envío gratis Amazon Fresh', en: 'Free shipping Amazon Fresh' },
  'premium.coupons':           { es: 'Cupones exclusivos',   en: 'Exclusive coupons' },
  'premium.loading':           { es: 'Cargando...',          en: 'Loading...' },

  // ── Alerts / confirmations (top bar) ─────────────────────────────────────
  'alert.loginTheme':          { es: 'Inicia sesión para cambiar el tema.', en: 'Please log in to change the theme.' },
  'alert.premiumTheme':        { es: 'Los temas Verde y Oscuro son exclusivos de Premium. ¡Hazte premium para desbloquearlos!', en: 'Green and Dark themes are Premium-exclusive. Upgrade to unlock them!' },
  'alert.cancelConfirm':       { es: '¿Seguro que quieres cancelar tu suscripción Premium? Perderás acceso a los temas exclusivos y los cupones.', en: 'Are you sure you want to cancel your Premium subscription? You will lose access to exclusive themes and coupons.' },
  'alert.newCardNumber':       { es: 'Introduce el nuevo número de tarjeta:', en: 'Enter your new card number:' },
  'alert.cardForPremium':      { es: 'Introduce tu número de tarjeta para activar Premium:', en: 'Enter your card number to activate Premium:' },
  'alert.noRecipes':           { es: 'No hay recetas aún.', en: 'No recipes yet.' },
  'alert.randomError':         { es: 'Error al buscar receta aleatoria.', en: 'Error fetching random recipe.' },

  // ── Bottom bar ────────────────────────────────────────────────────────────
  'nav.home':    { es: 'Inicio',  en: 'Home' },
  'nav.search':  { es: 'Buscar',  en: 'Search' },
  'nav.tables':  { es: 'Tables',  en: 'Tables' },
  'nav.profile': { es: 'Perfil',  en: 'Profile' },

  // ── Home page ─────────────────────────────────────────────────────────────
  'home.searchPlaceholder': { es: 'Busca recetas, ingredientes...', en: 'Search recipes, ingredients...' },
  'home.chipAll':      { es: 'Todo',       en: 'All' },
  'home.chipPasta':    { es: '🍝 Pasta',   en: '🍝 Pasta' },
  'home.chipSalads':   { es: '🥗 Ensaladas', en: '🥗 Salads' },
  'home.chipDesserts': { es: '🍰 Postres', en: '🍰 Desserts' },
  'home.chipMexican':  { es: '🌮 Mexicana', en: '🌮 Mexican' },
  'home.chipAsian':    { es: '🍜 Asiática', en: '🍜 Asian' },
  'home.chipMeat':     { es: '🥩 Carnes',  en: '🥩 Meat' },
  'home.noRecipes':    { es: 'No hay recetas para esta categoría aún.', en: 'No recipes in this category yet.' },
  'home.anonymous':    { es: 'Anónimo',    en: 'Anonymous' },
  'home.loginLike':    { es: 'Inicia sesión para dar like. ¿Ir al login?', en: 'Log in to like recipes. Go to login?' },

  // ── Search page ───────────────────────────────────────────────────────────
  'search.placeholder': { es: 'Buscar recetas o @usuarios...', en: 'Search recipes or @users...' },
  'search.btn':         { es: 'Buscar',    en: 'Search' },
  'search.tabRecipes':  { es: 'Recetas',   en: 'Recipes' },
  'search.tabUsers':    { es: 'Usuarios',  en: 'Users' },
  'search.noRecipes':   { es: 'No hay recetas para',  en: 'No recipes for' },
  'search.noUsers':     { es: 'No hay usuarios para', en: 'No users for' },

  // ── Login page ────────────────────────────────────────────────────────────
  'login.title':       { es: 'Iniciar Sesión - Trastevere', en: 'Login - Trastevere' },
  'login.welcome':     { es: 'Bienvenido',   en: 'Welcome' },
  'login.email':       { es: 'Email',        en: 'Email' },
  'login.emailPh':     { es: 'correo@ejemplo.com', en: 'email@example.com' },
  'login.password':    { es: 'Contraseña',   en: 'Password' },
  'login.passwordPh':  { es: 'Tu contraseña', en: 'Your password' },
  'login.btn':         { es: 'Entrar',       en: 'Log in' },
  'login.noAccount':   { es: '¿No tienes cuenta?', en: "Don't have an account?" },
  'login.register':    { es: 'Regístrate gratis', en: 'Sign up for free' },
  'login.errorEmpty':  { es: 'Por favor, completa todos los campos.', en: 'Please fill in all fields.' },
  'login.errorFailed': { es: 'Correo o contraseña incorrectos.', en: 'Incorrect email or password.' },

  // ── Register page ─────────────────────────────────────────────────────────
  'register.title':    { es: 'Registro - Trastevere', en: 'Register - Trastevere' },
  'register.heading':  { es: 'Crear Cuenta',   en: 'Create Account' },
  'register.username': { es: 'Usuario',        en: 'Username' },
  'register.usernamePh': { es: 'Tu nombre de usuario', en: 'Your username' },
  'register.email':    { es: 'Email',          en: 'Email' },
  'register.emailPh':  { es: 'correo@ejemplo.com', en: 'email@example.com' },
  'register.password': { es: 'Contraseña',     en: 'Password' },
  'register.passwordPh': { es: 'Contraseña segura', en: 'Secure password' },
  'register.premium':  { es: '✨ Activar Plan Premium', en: '✨ Activate Premium Plan' },
  'register.premiumTitle': { es: '✨ Plan Premium', en: '✨ Premium Plan' },
  'register.premiumInfo':  { es: 'Tras registrarte serás redirigido a la pasarela de pago segura (1,99€/mes).', en: 'After registering you will be redirected to the secure payment gateway (€1.99/month).' },
  'register.hasAccount': { es: '¿Ya tienes cuenta?', en: 'Already have an account?' },
  'register.login':      { es: 'Inicia sesión',      en: 'Log in' },
  'register.dni':      { es: 'DNI',            en: 'ID Number' },
  'register.dniPh':    { es: '12345678Z',      en: '12345678Z' },
  'register.phone':    { es: 'Teléfono',       en: 'Phone' },
  'register.phonePh':  { es: '600000000',      en: '600000000' },
  'register.card':     { es: 'Número de Tarjeta', en: 'Card Number' },
  'register.cardPh':   { es: '1234 5678 1234 5678', en: '1234 5678 1234 5678' },
  'register.btn':      { es: 'Registrarse',    en: 'Sign up' },

  // ── Profile page ──────────────────────────────────────────────────────────
  'profile.picHint':       { es: 'Toca tu foto para cambiarla', en: 'Tap your photo to change it' },
  'profile.recipes':       { es: 'Recetas',    en: 'Recipes' },
  'profile.followers':     { es: 'Seguidores', en: 'Followers' },
  'profile.following':     { es: 'Siguiendo',  en: 'Following' },
  'profile.stars':         { es: '⭐ Estrellas', en: '⭐ Stars' },
  'profile.email':         { es: 'Email',      en: 'Email' },
  'profile.phone':         { es: 'Teléfono',   en: 'Phone' },
  'profile.dni':           { es: 'DNI',        en: 'ID' },
  'profile.plan':          { es: 'Plan',       en: 'Plan' },
  'profile.phonePh':       { es: 'Sin configurar', en: 'Not set' },
  'profile.dniPh':         { es: 'Sin configurar', en: 'Not set' },
  'profile.edit':          { es: 'Editar',     en: 'Edit' },
  'profile.myProfile':     { es: 'Mi perfil',  en: 'My profile' },
  'profile.info':          { es: 'Info',       en: 'Info' },
  'profile.logout':        { es: 'Salir',      en: 'Log out' },
  'profile.saveChanges':   { es: 'Guardar cambios', en: 'Save changes' },
  'profile.joinTitle':     { es: '¡Únete a Trastevere!', en: 'Join Trastevere!' },
  'profile.joinSub':       { es: 'Crea tu red de recetas y guarda tus favoritos.', en: 'Build your recipe network and save your favourites.' },
  'profile.login':         { es: 'Iniciar Sesión', en: 'Log in' },
  'profile.createAccount': { es: 'Crear cuenta gratis', en: 'Create free account' },
  'profile.aboutTitle':    { es: 'Trastevere App', en: 'Trastevere App' },
  'profile.version':       { es: 'Versión:',   en: 'Version:' },
  'profile.build':         { es: 'Build:',     en: 'Build:' },
  'profile.authors':       { es: 'Autores:',   en: 'Authors:' },
  'profile.close':         { es: 'Cerrar',     en: 'Close' },
  'profile.updated':       { es: 'Perfil actualizado', en: 'Profile updated' },
  'profile.uploadError':   { es: 'Error al subir la imagen', en: 'Error uploading image' },

  // ── Create recipe page ────────────────────────────────────────────────────
  'create.title':        { es: 'Crear receta - Trastevere', en: 'Create recipe - Trastevere' },
  'create.heading':      { es: 'Nueva Receta', en: 'New Recipe' },
  'create.photoHint':    { es: '* Al menos una foto es obligatoria', en: '* At least one photo is required' },
  'create.titlePh':      { es: 'Título de la receta *', en: 'Recipe title *' },
  'create.descPh':       { es: 'Cuéntanos sobre tu plato... *', en: 'Tell us about your dish... *' },
  'create.ingredients':  { es: 'Ingredientes', en: 'Ingredients' },
  'create.addIngr':      { es: '+ Añadir ingrediente', en: '+ Add ingredient' },
  'create.tags':         { es: 'Tags',         en: 'Tags' },
  'create.tagsPh':       { es: 'Ej: pasta, italiano, rápido', en: 'e.g.: pasta, italian, quick' },
  'create.steps':        { es: 'Pasos de preparación', en: 'Preparation steps' },
  'create.addStep':      { es: '+ Añadir paso', en: '+ Add step' },
  'create.publish':      { es: '🍅 Publicar Receta', en: '🍅 Publish Recipe' },
  'create.login':        { es: 'Iniciar Sesión', en: 'Log in' },
  'create.createAccount':{ es: 'Crear cuenta gratis', en: 'Create free account' },
  'create.ingrQtyPh':    { es: 'Cant.', en: 'Qty.' },
  'create.ingrUnitPh':   { es: 'Unidad', en: 'Unit' },
  'create.ingrNamePh':   { es: 'Ingrediente', en: 'Ingredient' },
  'create.stepPh':       { es: 'Describe el paso', en: 'Describe the step' },
  'create.success':      { es: '¡Receta publicada con éxito!', en: 'Recipe published successfully!' },
  'create.errorTitle':   { es: 'El título es obligatorio.', en: 'Title is required.' },
  'create.errorDesc':    { es: 'La descripción es obligatoria.', en: 'Description is required.' },
  'create.errorPhoto':   { es: 'Debes subir al menos una foto.', en: 'You must upload at least one photo.' },
  'create.errorIngr':    { es: 'Debes añadir al menos un ingrediente.', en: 'You must add at least one ingredient.' },
  'create.errorSteps':   { es: 'Debes añadir al menos un paso.', en: 'You must add at least one step.' },
  'create.errorFix':     { es: 'Por favor corrige lo siguiente:', en: 'Please fix the following:' },
  'create.serverError':  { es: 'Error al conectar con el servidor.', en: 'Error connecting to the server.' },
  'create.publishError': { es: 'No se pudo publicar', en: 'Could not publish' },

  // ── Tables page ───────────────────────────────────────────────────────────
  'tables.title':        { es: 'Mis Tables - Trastevere', en: 'My Tables - Trastevere' },
  'tables.heading':      { es: 'Mis Tables', en: 'My Tables' },
  'tables.newPh':        { es: 'Nombre de la nueva table', en: 'New table name' },
  'tables.create':       { es: 'Crear', en: 'Create' },
  'tables.organize':     { es: 'Organiza tus colecciones', en: 'Organise your collections' },
  'tables.login':        { es: 'Iniciar Sesión', en: 'Log in' },
  'tables.createAccount':{ es: 'Crear cuenta gratis', en: 'Create free account' },
  'tables.empty':        { es: 'Aún no hay recetas guardadas aquí.', en: 'No recipes saved here yet.' },
  'tables.noTables': { es: 'Aún no tienes ninguna Table. ¡Crea la primera arriba!', en: "You don't have any Tables yet. Create your first one above!" },
  'tables.saved':        { es: 'recetas guardadas', en: 'saved recipes' },

  // ── Recipe detail page ────────────────────────────────────────────────────
  'recipe.notFound':     { es: 'Receta no encontrada',   en: 'Recipe not found' },
  'recipe.saveBtn':      { es: 'Guardar en Table',        en: 'Save to Table' },
  'recipe.saveTitle':    { es: 'Guardar en Table',        en: 'Save to Table' },
  'recipe.ingredients':  { es: 'Ingredientes',            en: 'Ingredients' },
  'recipe.steps':        { es: 'Pasos',                   en: 'Steps' },
  'recipe.anonymous':    { es: 'Cocinero Anónimo',        en: 'Anonymous Cook' },
  'recipe.loginSave':    { es: 'Inicia sesión para guardar recetas', en: 'Log in to save recipes' },
  'recipe.createTable':  { es: 'Crear mi primera Table',  en: 'Create my first Table' },
  'recipe.edit':   { es: 'Editar', en: 'Edit' },
  'recipe.delete': { es: 'Borrar', en: 'Delete' },
  'recipe.chooseTable': { es: 'Elige una table', en: 'Choose a table' },

  // ── Public profile page ───────────────────────────────────────────────────
  'public.recipes':      { es: 'Recetas',    en: 'Recipes' },
  'public.followers':    { es: 'Seguidores', en: 'Followers' },
  'public.following':    { es: 'Siguiendo',  en: 'Following' },
  'public.follow':       { es: 'Seguir',     en: 'Follow' },
  'public.unfollow':     { es: 'Siguiendo',  en: 'Following' },
  'public.noRecipes':    { es: 'Aún no hay recetas publicadas.', en: 'No recipes published yet.' },
  'public.noFollowers': { es: 'Aún no hay seguidores.', en: 'No followers yet.' },
  'public.noFollowing': { es: 'No sigue a nadie todavía.', en: 'Not following anyone yet.' },
  'public.rating':      { es: 'Valorar', en: 'Rate' },
  'public.yourRating':  { es: 'Tu valoración:', en: 'Your rating:' },
  'public.updated':     { es: '✓ Actualizada', en: '✓ Updated' },
  'public.saved':       { es: '✓ Guardada', en: '✓ Saved' },
};

// ── Core helpers ──────────────────────────────────────────────────────────────
function getLanguage() {
  return localStorage.getItem('trastevere_lang') || 'es';
}

function t(key) {
  const lang  = getLanguage();
  const entry = TRANSLATIONS[key];
  if (!entry) { console.warn('[i18n] Missing key:', key); return key; }
  return entry[lang] || entry['es'] || key;
}

// ── DOM application ───────────────────────────────────────────────────────────
// Elements that carry a data-i18n attribute get their textContent replaced.
// Elements with data-i18n-placeholder get their placeholder attribute replaced.
// Elements with data-i18n-title get their title attribute replaced.
function applyLanguage() {
  const lang = getLanguage();

  // Text content
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const val = t(key);
    if (val !== key) el.textContent = val;
  });

  // Placeholders
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    const val = t(key);
    if (val !== key) el.placeholder = val;
  });

  // Title attributes (tooltips)
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const key = el.getAttribute('data-i18n-title');
    const val = t(key);
    if (val !== key) el.title = val;
  });

  // Update <html lang="…"> for accessibility
  document.documentElement.lang = lang;

  // Update the settings <select> to reflect the current choice
  const sel = document.querySelector('.lang-select');
  if (sel) sel.value = lang;
}

// ── Auto-apply on every page load ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', applyLanguage);