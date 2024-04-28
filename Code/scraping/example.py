from bs4 import BeautifulSoup 

with open("index.html", "r") as f:
  data = f.read()

#print(data)

soup = BeautifulSoup(data, 'html.parser')

#print(soup)


divs = soup.select("div")

print(len(divs), "divs found")

for d in divs:
  print()
  print(d)



print("content:", divs[0].get_text())


div2 = divs[1]

pps = div2.select("p")

print("PPS:")

for p in pps:
  #print(p.get_text())
  pass


print("dailies:")
dailies = soup.select(".daily")
for f in dailies:
  print(d.get_text())

print(dailies[1].attrs['data-value']) 