import axios from "axios";

// const axiosInstance = axios.create({
//     baseURL: 'http://127.0.0.1:5000',
//     timeout: 1000,
   
//   })


  const axiosInstance = axios.create({
    baseURL: 'https://dlqtl97sug.execute-api.eu-north-1.amazonaws.com/v1',
    timeout: 5000,
   
  })

export {axiosInstance}