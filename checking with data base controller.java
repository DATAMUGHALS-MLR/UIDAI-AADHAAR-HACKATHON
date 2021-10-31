public class HomeController : Controller
{
    private DBCtx Context { get; }
    public HomeController(DBCtx _context)
    {
        this.Context = _context;
    }
 
    public IActionResult Index()
    {
        return View();
    }
 
    [HttpPost]
    public IActionResult Index(string name)
    {
        AadharID = Context.AadharID.Where(x => x.Address== name).FirstOrDefault();
        if (customer != null)
        {
            ViewBag.Message = "Exist";
            return View();
        }
        else
        {
            return View(customer);
        }
    }
}