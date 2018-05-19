# Table of contents
 0. Goal  
 1. How web framework works  
   1.1. WSGI  
   1.2. Request & Response  
   1.3. Routing  
   1.4. Flask code  
   1.5. Other topic  
   1.6. Reference  
 2. Build an simple app using Flask & React  
   2.1. First Flask app  
   2.2. Template  
   2.3. Create a more complex page  
   2.4. Restful  
   2.5. Reference  
   2.6. Other  
 3. Deploy to AWS / Azure  
 4. Other topics  
   3.1. Project structure  
   2.2. Design database  
   3.3. Login
   3.4. Blueprint  
   3.5. Reference  
   3.6. Custom your bootstrap
   3.7. NPM front-end package managerment  
 5. Other frameworks  
   4.1. ASP.net  
   4.2. Spring  
 6. Open source reference
   6.1 Bootstrap
   6.2 React
   6.3 Flask
   6.4 Flask web site


# Goal
通过实现一个简单的类似Instagram的网站学习构建网站的整套技术，包括前端和后端。主要使用Python，Flask，React和TypeScript等技术，目标是获得开发的体验，为后面深入学习提供感性的认识。


# How web framework works
一个Web App可以概括为：收到一个http请求，返回所请求的内容。要做到这点，不一定要使用Web framework，在Python里一个简单的WSGI的应用就能做到。但是以WSGI应用的方式构建Web App其效率是非常低的，所以我们会用到Web framework。它对WSGI进行了封装，并还提供了很多额外的功能，比如Session，Request和Response的抽象，路由（Routing）等等。  
  
下面会从一个简单的WSGI应用讲起，并构建简单的Web framework，进而延伸到Flask这个轻量级的框架。  


## WSGI
在Java中类似的概念是Servlet，而Asp.Net/C#中类似的概念是HttpHandler。  

Python里的WSGI样例
``` python
def application(environ, start_response):
    status = '200 OK'                   # Status code ref: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    headers = [('Content-Type', 'text/html; charset=utf8')]
    start_response(status, headers)
    return [b"Meng Jiang is smart"]     # WSGI requires to return iterable bytes literal
```
这部分代码可以参考 1.1._wsgi/wsgi_demo.py . 要运行程序，可以执行以下命令：
``` shell
python ./1.1._wsgi/demo.py --ip <your-ip-address> --port <your-port-number>
```
然后打开浏览器访问以下网址：http://&lt;your-ip-address&gt;:&lt;your-port-number&gt;/Routing/Demo?parameter=value  
在environ的'PATH\_INFO'中可以找到路由‘Routing/Demo’，而在‘QUERY\_STRING’中可以找到参数‘Parameter=value’。也就是environ里面包含了我们处理一个Request所需的信息，后面我们会看到一个Web Framework是怎么利用这些信息帮助我们构建Web App的。

Java里的Servlet样例
``` java
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class HelloServlet extends HttpServlet {
 
  private String message;

  public void init() throws ServletException
  {
      message = "Hello World";
  }

  public void doGet(HttpServletRequest request,
                    HttpServletResponse response)
            throws ServletException, IOException
  {
      response.setContentType("text/html");

      PrintWriter out = response.getWriter();
      out.println("<h1>" + message + "</h1>");
  }
  
  public void destroy()
  {
      // nothing needs to be done in this case
  }
}
```
具体可以参考：[Servlet 实例](http://www.runoob.com/servlet/servlet-first-example.html 'Servlet实例')

C#里的HttpHandler样例
``` c#
using System.Web;
public class HelloHTTPHandler : IHttpHandler
{
    public HelloHTTPHandler()
    {
    }

    public void ProcessRequest(HttpContext context)
    {
        HttpRequest Request = context.Request;
        HttpResponse Response = context.Response;
        // This handler is called whenever a file ending 
        // in .sample is requested. A file with that extension
        // does not need to exist.
        Response.Write("<html>");
        Response.Write("<body>");
        Response.Write("<h1>Hello from a synchronous custom HTTP handler.</h1>");
        Response.Write("</body>");
        Response.Write("</html>");
    }

    public bool IsReusable
    {
        // To enable pooling, return true here.
        // This keeps the handler in memory.
        get { return false; }
    }
}
```
具体可以参考：[MSDN - Walkthrough: Creating a Synchronous HTTP Handler](https://msdn.microsoft.com/en-us/library/ms228090.aspx 'MSDN')


## Request & Response 
打开浏览器访问以下网址：http://&lt;your-ip-address&gt;:&lt;your-port-number&gt;/any/route?name=Meng-Jiang


## Routing
打开浏览器访问以下网址：http://&lt;your-ip-address&gt;:&lt;your-port-number&gt;/say/something/professional?name=Meng-Jiang


## Flask code  
在Flask的Github repo里面能够找到我们Web Framework对应功能的代码样例。  

Flask是基于werkzeug构建的，werkzeug是一个WSGI库，提供了很多WSGI应用所需的Utility函数。在werkzeug的Github repo里能够找到对应的Request和Response的实现：
``` python
# code: https://github.com/pallets/werkzeug/blob/master/werkzeug/wrappers.py
class BaseRequest(object):

  ...

  @cached_property
  def args(self):
      """The parsed URL parameters (the part in the URL after the question
      mark).
      By default an
      :class:`~werkzeug.datastructures.ImmutableMultiDict`
      is returned from this function.  This can be changed by setting
      :attr:`parameter_storage_class` to a different type.  This might
      be necessary if the order of the form data is important.
      """
      return url_decode(wsgi_get_bytes(self.environ.get('QUERY_STRING', '')),
                        self.url_charset, errors=self.encoding_errors,
                        cls=self.parameter_storage_class)


class BaseResponse(object):
	
  ...

  def __call__(self, environ, start_response):
      """Process this response as WSGI application.
      :param environ: the WSGI environment.
      :param start_response: the response callable provided by the WSGI
                             server.
      :return: an application iterator
      """
      app_iter, status, headers = self.get_wsgi_response(environ)
      start_response(status, headers)
      return app_iter
```

再比如Routing，你可以在 https://github.com/pallets/flask/blob/master/flask/app.py 的def route(self, rule, **options)函数中找到实现Routing的代码：  

``` python
def route(self, rule, **options):
    """A decorator that is used to register a view function for a
    given URL rule.  This does the same thing as :meth:`add_url_rule`
    but is intended for decorator usage::
        @app.route('/')
        def index():
            return 'Hello World'
    For more information refer to :ref:`url-route-registrations`.
    :param rule: the URL rule as string
    :param endpoint: the endpoint for the registered URL rule.  Flask
                     itself assumes the name of the view function as
                     endpoint
    :param options: the options to be forwarded to the underlying
                    :class:`~werkzeug.routing.Rule` object.  A change
                    to Werkzeug is handling of method options.  methods
                    is a list of methods this rule should be limited
                    to (``GET``, ``POST`` etc.).  By default a rule
                    just listens for ``GET`` (and implicitly ``HEAD``).
                    Starting with Flask 0.6, ``OPTIONS`` is implicitly
                    added and handled by the standard request handling.
    """
    def decorator(f):                                     # 定义decorator
        endpoint = options.pop('endpoint', None)
        self.add_url_rule(rule, endpoint, f, **options)   # 符合rule（文档中@app.route('/')中的'/'）的请求  
                                                          # 将会由函数f（文档中的def index()）处理，  
                                                          # 并返回处理后的html文档
        return f
    return decorator
```


## Other topic
TCP & UDP  
Multi processor/thread  
Session  
Database  
Template  

## Reference
* [Build Python Web Framework](http://ningning.today/2017/08/05/web/build-python-web-framework/ 'Implement a web framework')


# Build an simple app using Flask & React  

我们这里后端使用的是Flask框架，它实现了路由，Requst/Response的抽象，Session，页面在Server-side的渲染，登录验证等等功能。

前端的框架可以分为两类：CSS框架和JavaScript框架。

CSS框架负责展现，一般会提供各种各样的UI组件比如：按钮，表格，下拉列表，警告框，Tab，字体排版，Carousel等等。我们这里使用Bootstrap。

JavaScript负责交互，JavaScript框架能够帮助我们更好地达到这个目标。过去我们常常是在Server渲染页面，然后返回渲染好的页面给用户，这样大多数的运算负载都发生在Server端，另一种方式是在Server端构建Restful的API，Client通过调用这些API获得所需的数据，并利用这些数据对页面进行渲染。JavaScript为达到这个目标通常会提供的功能：  
1. Client-side routing  
2. templating  
3. 第一轮的model validation  
4. 构建表格  
5. 分页   

Javascript框架这里我们使用Angular，由谷歌维护。其他well-support的框架有React，由facebook维护。


## First Flask app  
执行以下命令：
``` shell
FLASK_APP=./2.1._FirstFlaskApp/demo.py python -m flask run --host=<your-ip-address> --port=<your-port-number>
```
然后打开浏览器访问以下网址：http://&lt;your-ip-address&gt;:&lt;your-port-number&gt;/


## Template
执行以下命令：
``` shell
FLASK_APP=./2.2._Template/demo.py python -m flask run --host=<your-ip-address> --port=<your-port-number>
```
然后打开浏览器访问以下网址：http://&lt;your-ip-address&gt;:&lt;your-port-number&gt;/

有了Template我们终于可以开始构建一个稍微复杂一点的页面了。

## Create a more complex page  

这部分主要需要的是HTML和CSS的知识。 

为了方便开发，我么使用Flask的Debug模式，这样每次访问页面会重新加载资源文件，这样我们的修改在能够即时反映出来。但是注意浏览器会做一定的Cache导致某些改动没有立即显示出来，这时可以使用Incognito / Private Mode。

执行以下命令来启动我们的应用
```shell
FLASK_DEBUG=1 FLASK_APP=./2.3._Complex/demo.py python -m flask run --host=10.123.150.78 --port=7777
```

可以看到这个终于有点像我们平时看到的网站了，暂时并没有使用到除了HTML和CSS之外的内容，后面会尝试新的技术。

在这个例子里我们使用了Bootstrap这个css框架，我们主要用到了Tab-Pane组件，Carousel组件和Card组件。整个应用都只包含一个页面，我们称为Single Page Application（SAP），当然通常意义上的SAP应用会使用JS来跟服务器交互，在客户端动态渲染页面。Card组件帮助我们实现了瀑布流的效果（Masonry Layouts），这是图片类应用常用的布局，能够将不同尺寸的图片自然地排版到同一个页面。

Bootstrap框架帮助我们轻易地构建Responsive的网页，也就是整个页面会根据访问设备的尺寸自适应地调整布局，适应PC和Mobile端的访问。尝试调整浏览页的窗口宽度体会这个功能。  

## Restful

上一个例子内容是静态的，没有用到实时的渲染，每次添加新的图片都要修改模板文件。一般的做法是从数据库中读取资源（比如图片），然后动态地构造整个页面并渲染出来，这个功能就是我们之前提到的模板。模板功能既可以在服务器端实现，也可以在客户端实现。这个样例将会构建一个Restful的API，客户端调用API获取所需的资源，并动态渲染展现给用户。  


## Other  

Bootstrap有很多收费的Theme，可以学习其中的设计，参考[Bootstrap Themes](https://themes.getbootstrap.com/ 'bootstrap themes')  

Chrome的开发者工具有Device Mode可以方便测试手机的显示效果，参考[Chrome Device Mode](https://developers.google.com/web/tools/chrome-devtools/device-mode/?hl=zh-tw 'Chrome Device Mode')  

Carousel对于不等边长的图片处理比较麻烦，图片尺寸变了整个布局就变了，最好是服务器存有一份等边长的图片，比如高度都一样的图片，方便在Carousel中显示。  

## Reference  
[Rest API Best Practice](http://polyglot.ninja/rest-api-best-practices-python-flask-tutorial/ 'Rest API Best Practice')  
[使用Python和Flask设计Restful API](http://www.pythondoc.com/flask-restful/first.html 'Restful API with Flask')  
[A Beginner's Guide to CSS Front End Frameworks](https://blog.zipboard.co/a-beginners-guide-to-css-front-end-frameworks-8045a499456b 'A Beginner\'s Guide to CSS Front End Frameworks')  
[The What and Why of Javascript Frameworks](https://artandlogic.com/2015/05/the-what-and-why-of-javascript-frameworks/ 'The What and Why of Javascript Frameworks')  
[Boostrap Sample of Different Layout](https://v4-alpha.getbootstrap.com/examples/ 'Bootstrap Sample')
[Single Page Application](https://en.wikipedia.org/wiki/Single-page_application 'Single Page Application')  
