const toSnakeCase = (str: string): string => 
    str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
  
  const convertCamelToSnakeCase = (obj: Record<string, any>): Record<string, any> => {
    const newObj: Record<string, any> = {};
    Object.keys(obj).forEach(key => {
      newObj[toSnakeCase(key)] = obj[key];
    });
    return newObj;
  };
  
  export default convertCamelToSnakeCase;