# Table of contents
 0. Goal  
 1. How web framework works  
   1.1. WSGI  
   1.2. Request & Response  
   1.3. Routing  
   1.4. Flask  
   1.5. Other topic  
   1.6. Reference  
 2. Build an simple app using Flask & React  
   2.1. First Flask app  
   2.2. Create a complexer page  
   2.3. Inter-action  
   2.4. Create more pages  
   2.5. Design database  
   2.6. Restful  
   2.7. Reference  
 3. Other topics  
   3.1. Project structure  
   3.2. ORM  
   3.3. Blueprint  
   3.4. Reference  
 4. Other frameworks  
   4.1. ASP.net  
   4.2. Spring  


# Goal
通过实现一个简单的类似Instagram的网站学习构建网站的整套技术，包括前端和后端。主要使用Python，Flask，React和TypeScript等技术，目标是获得开发的体验，为后面深入学习提供感性的认识。


# How web framework works
一个Web App可以概括为：收到一个http请求，返回所请求的内容。要做到这点，不一定要使用Web framework，一个简单的WSGI的应用就能做到。但是以WSGI应用的方式构建Web App其效率是非常低的，所以我们会用到Web framework。它对WSGI进行了封装，并还提供了很多额外的功能，比如Request和Response的抽象，路由（Routing）等等。  
  
下面会从一个简单的WSGI应用讲起，并构建简单的Web framework，进而延伸到Flask这个轻量级的框架。  

## WSGI


## Reference
* [http://ningning.today/2017/08/05/web/build-python-web-framework/](http://ningning.today/2017/08/05/web/build-python-web-framework/ 'Implement a web framework')
