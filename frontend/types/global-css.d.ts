// Global CSS declaration for side effect imports
declare module '*.css' {
  const content: { [key: string]: any };
  export default content;
}

// Declaration for global CSS files imported as side effects
declare module '*.global.css' {
  const content: { [key: string]: any };
  export default content;
}