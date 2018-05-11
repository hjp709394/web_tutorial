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
打开浏览器访问以下网址：http://&lt;your-ip-address&gt;:&lt;your-port-number&gt;/any/route?name=MengJiang


## Routing
打开浏览器访问以下网址：http://&lt;your-ip-address&gt;:&lt;your-port-number&gt;/say/something/professional?name=MengJiang


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
