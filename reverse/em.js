const detector = function () {
  function hasProp(obj, prop) { return prop in obj; }
  function boolToBit(bool) { return bool ? 1 : 0; }
  function checkGetter(bool) { return bool ? 2 : 1; }

  const FALSE = 0, TRUE = 1, GETTER = 2;
  const typeOf = (val) => typeof val;
  const isFunction = (fn) => typeOf(fn) === 'function';

  const checks = [
    ['ph', checkPhantom],
    ['cp', checkCallPhantom],
    ['ek', checkErrorKeys],
    ['wd', checkWebDriver],
    ['nt', checkNightmare],
    ['si', checkScriptFn],
    ['sc', checkSeleniumMarker]
  ];

  function checkPhantom() {
    return boolToBit(hasProp(window, '_phantom')); // PhantomJS detection
  }

  function checkCallPhantom() {
    if (!hasProp(window, 'callPhantom')) return FALSE;
    try { window.callPhantom; } catch (e) { return 9; } // PhantomJS throws when accessed
    return TRUE;
  }

  function checkErrorKeys() {
    // Checks if error stack properties exist (common in headless environments)
    const errProps = ['line', 'column', 'lineNumber', 'columnNumber', 'fileName', 'message', 'number', 'description', 'sourceURL', 'stack'];
    const results = errProps.map(prop => boolToBit(hasProp(new Error(), prop)));
    return parseInt(results.join(''), 2).toString(16); // Converts to hex
  }

  function checkWebDriver() {
    // Detects `navigator.webdriver` (Selenium/Chrome Headless)
    if (!hasProp(navigator, 'webdriver')) return FALSE;
    const descriptor = Object.getOwnPropertyDescriptor(navigator, 'webdriver');
    return descriptor?.get ? GETTER : TRUE; // Checks if it's a getter
  }

  function checkNightmare() {
    return boolToBit(hasProp(window, '_nightmare')); // Nightmare.js detection
  }

  function checkScriptFn() {
    return boolToBit(hasProp(document, '_webdriverScriptFn')); // Selenium internal
  }

  function checkSeleniumMarker() {
    return boolToBit(hasProp(document, '$cdc_asdjflasutopfhvcZLmcfl_')); // Selenium marker
  }

  return function (results = {}) {
    checks.forEach(([key, check]) => {
      results[key] = check();
    });
    return results;
  };
}();
//this will onyl work in browsers
console.log(detector([], {}));