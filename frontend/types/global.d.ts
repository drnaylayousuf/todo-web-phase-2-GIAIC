// Global type declarations

// CSS modules
declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

// Global CSS imports (side effect imports)
declare module '*.css' {
  const content: any;
  export default content;
}

declare module '*.scss' {
  const content: any;
  export default content;
}

declare module '*.sass' {
  const content: any;
  export default content;
}

declare module '*.less' {
  const content: any;
  export default content;
}

declare module '*.styl' {
  const content: any;
  export default content;
}