var aFriend = "Beuno";
var date = DateTime.Now;

if (aFriend == "Beuno")
{
    Console.WriteLine("Eita, é o Beuno! Que bom te ver por aqui!");
}
else {

    Console.WriteLine("-------------------------------------------------------------------------");
    Console.WriteLine($"Hello my frind {aFriend}! Today is {date.DayOfWeek}, it´s {date:HH:mm} now.");
    Console.WriteLine("-------------------------------------------------------------------------");
}
Console.WriteLine(" ");

var counter = 0;
Console.WriteLine("While loop: ");
while(counter <15)
    {
        Console.WriteLine($"Counter is {counter}");
        counter++;
    };
Console.WriteLine(" ");

Console.WriteLine("Do-While loop: ");
do
    {
        Console.WriteLine($"Counter is {counter}");
        counter++;
    }
    while(counter <15);

Console.WriteLine(" ");
Console.WriteLine("For loop:");
for ( counter = 0; counter <10; counter++)
{
    Console.WriteLine($"Counter is {counter}");
}
