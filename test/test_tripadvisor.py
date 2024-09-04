from bs4 import BeautifulSoup

from src.model.tripadvisor import TripAdvisor


def test_build_url():
    expected = "https://www.google.com/search?q=Home Slice Pizza Austin"
    actual = TripAdvisor.build_url("Home Slice Pizza", "Austin")
    assert actual == expected

def test_get_rating_and_review_count_tripadvisor():
    expected = ("4.5", "1,000")
    html =  '''
         <div><div class="Gx5Zad fP1Qef xpd EtOod pkphOe"><div class="egMi0 kCrYT"><a href="/url?esrc=s&amp;q=&amp;rct=j&amp;sa=U&amp;url=https://www.tripadvisor.com/Restaurant_Review-g30196-d18095194-Reviews-Home_Slice_Pizza-Austin_Texas.html&amp;ved=2ahUKEwjtp5f2_tiGAxXvk4kEHXjJC1YQFnoECAYQAg&amp;usg=AOvVaw3wB5AqT0vSUygUYJ5yg9Cl" data-ved="2ahUKEwjtp5f2_tiGAxXvk4kEHXjJC1YQFnoECAYQAg"><div class="DnJfK"><div class="j039Wc"><h3 class="zBAuLc l97dzf"><div class="BNeawe vvjwJb AP7Wnd">HOME SLICE PIZZA, Austin - 501 E 53rd St - Tripadvisor</div></h3></div><div class="sCuL3"><div class="BNeawe UPmit AP7Wnd lRVwie">www.tripadvisor.com › United States › Texas (TX) › Austin</div></div></div></a></div><div class="kCrYT"><div><div class="BNeawe s3v9rd AP7Wnd"><div><div class="v9i61e"><div class="BNeawe s3v9rd AP7Wnd"><span class="r0bn4c rQMQod">Rating</span> <span class="r0bn4c rQMQod tP9Zud"><span> </span><span aria-hidden="true" class="oqSTJd">4.5</span><span> </span><div class="Hk2yDb KsR1A" aria-label="Rated 4.5 out of 5" role="img"><span style="width:52px"></span></div><span> </span><span>(1,000)</span><span> </span></span> <span class="r0bn4c rQMQod"> · </span><span class="r0bn4c rQMQod">$$ - $$$</span></div></div><div><div class="BNeawe s3v9rd AP7Wnd">13 reviews#681 of 1,901 Restaurants in Austin$$ - $$$ItalianPizza. 501 E 53rd St, Austin, TX 78751-2103 +1 512-707-7437 Website. Closed now: See all hours.</div></div></div></div></div></div></div></div>
        '''
    page = BeautifulSoup(html, 'html.parser')
    actual = TripAdvisor.get_rating_and_review_count(page)
    assert actual == expected