import json
import re

output = '''
{'search_metadata': {'id': '64d830434055aa6183cebb38', 'status': 'Success', 'json_endpoint': 'https://serpapi.com/searches/1d4a53df43c88119/64d830434055aa6183cebb38.json', 'created_at': '2023-08-13 01:22:11 UTC', 'processed_at': '2023-08-13 01:22:11 UTC', 'google_url': 'https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&sourceid=chrome&ie=UTF-8', 'raw_html_file': 'https://serpapi.com/searches/1d4a53df43c88119/64d830434055aa6183cebb38.html', 'total_time_taken': 1.89}, 'search_parameters': {'engine': 'google', 'q': 'Caitlyn Guo', 'google_domain': 'google.com', 'device': 'desktop'}, 'search_information': {'organic_results_state': 'Results for exact spelling', 'query_displayed': 'Caitlyn Guo', 'total_results': 1220000, 'time_taken_displayed': 0.3, 'menu_items': [{'position': 1, 'title': 'Images', 'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQICxAB', 'serpapi_link': 'https://serpapi.com/search.json?device=desktop&engine=google_images&gl=us&google_domain=google.com&hl=en&q=Caitlyn+Guo'}, {'position': 2, 'title': 'News', 'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=nws&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQIChAB', 'serpapi_link': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&tbm=nws'}, {'position': 3, 'title': 'Videos', 'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=vid&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQICRAB', 'serpapi_link': 'https://serpapi.com/search.json?device=desktop&engine=google_videos&gl=us&google_domain=google.com&hl=en&q=Caitlyn+Guo'}, {'position': 4, 'title': 'Shopping', 'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=shop&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQIDBAB', 'serpapi_link': 'https://serpapi.com/search.json?device=desktop&engine=google_shopping&gl=us&google_domain=google.com&hl=en&q=Caitlyn+Guo'}, {'position': 5, 'title': 'Books', 'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=bks&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQIOBAB'}, {'position': 6, 'title': 'Maps', 'link': 'https://maps.google.com/maps?sca_esv=556415102&output=search&q=Caitlyn+Guo&source=lnms&entry=mc&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQIORAB'}, {'position': 7, 'title': 'Flights', 'link': 'https://www.google.com/travel/flights?sca_esv=556415102&output=search&q=Caitlyn+Guo&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQINxAB'}, {'position': 8, 'title': 'Finance', 'link': 'https://www.google.com/finance?sca_esv=556415102&output=search&q=Caitlyn+Guo&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQIOhAB'}]}, 'inline_images': [{'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgNEAA#imgrc=JZ4gPqNdLmaJmM', 'source': 'https://github.com/cbguo2', 'thumbnail': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab63115e21c470f7e08e5b260207796138b0f41e059a2287034742.jpeg', 'original': 'https://avatars.githubusercontent.com/u/42985049?v=4', 'title': 'cbguo2 (Caitlyn Guo) · GitHub', 'source_name': 'GitHub'}, {'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgPEAA#imgrc=-dOn-q5vcS6AaM', 'source': 'https://www.linkedin.com/in/cguo82', 'thumbnail': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab63116404133f2e49c28868985bbee2d6c134201a93ca159d142b.jpeg', 'original': 'https://media.licdn.com/dms/image/C4D03AQEyAf3ohwufaw/profile-displayphoto-shrink_800_800/0/1628880583050?e=2147483647&v=beta&t=AAe-VhgGx-_cpJb64t6SiHcveqzH0soLcudJTaXHvpw', 'title': 'Caitlyn Guo - Software Engineer - Uber | LinkedIn', 'source_name': 'LinkedIn'}, {'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgYEAA#imgrc=pogNSGyjcRi3eM', 'source': 'https://devpost.com/cbguo2', 'thumbnail': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab6311dbd8855353284a01c266c6fddae720aab5cb69b8e6875896.jpeg', 'original': 'https://d112y698adiu2z.cloudfront.net/photos/production/user_photos/000/770/874/datas/xlarge.png', 'title': "Caitlyn Guo's (cbguo2) software portfolio | Devpost", 'source_name': 'Devpost'}, {'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgSEAA#imgrc=cNlZJWpeZiwkjM', 'source': 'https://sg.linkedin.com/in/caitlyn-guo-yiyun-9a27751a8', 'thumbnail': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab631168cab74cf1f9d8af51e1e769987ac87e27cb6c152c3d2ce5.jpeg', 'original': 'https://media.licdn.com/dms/image/D5603AQHEchx4JZBl8A/profile-displayphoto-shrink_800_800/0/1669787270885?e=2147483647&v=beta&t=RVCunExh55aVZXhGEHPrGpfwdaApzJepr5OSO-TczLg', 'title': 'Caitlyn Guo Yiyun - Global Management Trainee - Qudian(趣店 ...', 'source_name': 'LinkedIn'}, {'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgUEAA#imgrc=eQgD-Nth5qtGOM', 'source': 'https://www.linkedin.com/in/cguo82', 'thumbnail': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab6311d913e9348da4099031fffe452bd353edf0f9067814e2bc1c.jpeg', 'original': 'https://media.licdn.com/dms/image/C4E22AQEakkyFLmvmIA/feedshare-shrink_800/0/1622418596388?e=2147483647&v=beta&t=J1lR2vytDrej0xGxEK_zte04z_5NuuC-budBrzD7v_0', 'title': 'Caitlyn Guo - Software Engineer - Uber | LinkedIn', 'source_name': 'LinkedIn'}, {'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgREAA#imgrc=NENm3o49jdNQcM', 'source': 'https://www.racked.com/2016/4/21/11477318/time-100-2016', 'thumbnail': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab631128289d7d3217add9335215ceffe48d37cdb412a079bfad73.jpeg', 'original': 'https://cdn.vox-cdn.com/thumbor/3KK8Bdwjq8Ad-RWR8dXephgLOyc=/60x0:2932x2154/1400x1050/filters:focal(60x0:2932x2154):format(jpeg)/cdn.vox-cdn.com/uploads/chorus_image/image/49366163/GettyImages-520691680.0.0.jpg', 'title': 'Karlie Kloss, Guo Pei, and Caitlyn Jenner Make the Time 100 ...', 'source_name': 'Racked'}, {'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgTEAA#imgrc=6cN3gqcYj_i3oM', 'source': 'https://twitter.com/CityofLdnOnt/status/1437880121797513238', 'thumbnail': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfW3eJhoYo4lJOZREz73MtR49TrWnKfAGESFnVbsIxvw&s', 'original': 'https://pbs.twimg.com/media/E_RgWYrWEAAHuUe.jpg', 'title': 'City of London on Twitter: "Congratulations to Cindy Sun ...', 'source_name': 'Twitter'}, {'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgXEAA#imgrc=5krV66uEYNn5_M', 'source': 'https://www.berkeleyubg.org/our-members', 'thumbnail': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEjuFVLtSKZrnNQE2juSWBQ4d6ymA9IhFgySi1qgYC&s', 'original': 'https://images.squarespace-cdn.com/content/v1/5ff6cf81cca0501131aedc5c/f0db8c8b-e911-4ec2-8933-7790542952d2/318248018_703932874448713_7612557329667606544_n.jpg', 'title': 'Members — Undergraduate Business Group', 'source_name': 'Undergraduate Business Group'}, {'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgOEAA#imgrc=H-BTKTrKqvvd-M', 'source': 'https://www.berkeleyubg.org/our-members', 'thumbnail': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBXkennsoVk-kpRnp-WJx1EJDRZ0iZn9NV1fcvc0fb&s', 'original': 'https://images.squarespace-cdn.com/content/v1/5ff6cf81cca0501131aedc5c/cac9f675-1be3-40b4-a279-cd62a8e1b921/322541198_972545480390608_2636439282626952368_n.jpg', 'title': 'Members — Undergraduate Business Group', 'source_name': 'Undergraduate Business Group'}, {'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgQEAA#imgrc=be0WY7RoWz-V2M', 'source': 'https://ucsdtritons.com/sports/fencing/roster/caitlyn-callaghan/2713', 'thumbnail': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSL5pvTKAlh_QuPcTa7uK2q0evuGGuJ6AmGCzv_sl2z&s', 'original': 'https://ucsdtritons.com/images/2017/11/21/FSXPTIIMHUBQXYK.20171121173910.jpg?width=300', 'title': 'Caitlyn Callaghan - 2017-18 - Fencing - UC San Diego', 'source_name': 'UC San Diego Athletics'}], 'inline_images_suggested_searches': [{'name': 'queen elizabeth', 'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&chips=q:caitlyn+guo,online_chips:queen+elizabeth:uf4Lr-R20qY%3D&usg=AI4_-kSpMXcn9_yLFOT5ljBATjAxOXXTAA&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQgIoDKAB6BAgZEBI', 'chips': 'q:caitlyn+guo,online_chips:queen+elizabeth:uf4Lr-R20qY%3D', 'serpapi_link': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo', 'thumbnail': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab63117c20c5e6a19e57e53482a23cbb6fcd6ffbf64653dd9005cb10ad5434c7947eaf1f1bcc944150573e.jpeg'}, {'name': 'scherba', 'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&chips=q:caitlyn+guo,online_chips:scherba&usg=AI4_-kRpkVtbG7W8W33H2tFR0uDVWlOGMg&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQgIoDKAF6BAgZEBY', 'chips': 'q:caitlyn+guo,online_chips:scherba', 'serpapi_link': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo'}, {'name': 'shilbayeh', 'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&chips=q:caitlyn+guo,online_chips:shilbayeh&usg=AI4_-kT1WpeMYdPkPzVvO3wLxGci6wzKdg&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQgIoDKAJ6BAgZEBk', 'chips': 'q:caitlyn+guo,online_chips:shilbayeh', 'serpapi_link': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo'}, {'name': 'elizabeth scholarship', 'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&chips=q:caitlyn+guo,online_chips:elizabeth+scholarship&usg=AI4_-kQys-FQ7te2alQxvYIEi7IKtbvCzA&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQgIoDKAN6BAgZEBw', 'chips': 'q:caitlyn+guo,online_chips:elizabeth+scholarship', 'serpapi_link': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo'}, {'name': 'software engineer', 'link': 'https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&chips=q:caitlyn+guo,online_chips:software+engineer:LnFvrvqn0_k%3D&usg=AI4_-kQivFbTOCC12VqzDWkldvNO0EInHA&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQgIoDKAR6BAgZEB8', 'chips': 'q:caitlyn+guo,online_chips:software+engineer:LnFvrvqn0_k%3D', 'serpapi_link': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo', 'thumbnail': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab63117c20c5e6a19e57e53482a23cbb6fcd6ffbf64653dd9005cb5fb263c26143176cb957f9612ce2bf00.jpeg'}], 'organic_results': [{'position': 1, 'title': 'Caitlyn Guo - Software Engineer - Uber', 'link': 'https://www.linkedin.com/in/cguo82', 'displayed_link': 'https://www.linkedin.com › cguo82', 'favicon': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b13848b6fdc706eafa2eca266e8f091ddf2795.png', 'snippet': 'View the profiles of professionals named "Caitlyn Guo" on LinkedIn. There are 2 professionals named "Caitlyn Guo", who use LinkedIn to exchange information, ...', 'snippet_highlighted_words': ['Caitlyn Guo', 'Caitlyn Guo'], 'about_this_result': {'keywords': ['caitlyn', 'guo'], 'languages': ['English'], 'regions': ['United States']}, 'rich_snippet_list': ['Software Engineer at Uber', 'Activity', 'Experience', 'Education', 'Volunteer Experience', 'Courses', 'Projects'], 'source': 'LinkedIn', 'related_results': [{'position': 1, 'title': '2 "Caitlyn Guo" profiles', 'link': 'https://www.linkedin.com/pub/dir/Caitlyn/Guo', 'displayed_link': 'https://www.linkedin.com › pub › dir › Caitlyn › Guo', 'snippet': 'View the profiles of professionals named "Caitlyn Guo" on LinkedIn. There are 2 professionals named "Caitlyn Guo", who use LinkedIn to exchange information, ...', 'snippet_highlighted_words': ['Caitlyn Guo', 'Caitlyn Guo'], 'about_this_result': {'keywords': ['caitlyn', 'guo'], 'languages': ['English'], 'regions': ['United States']}}]}, {'position': 2, 'title': 'Caitlin J. Guo, MD', 'link': 'https://med.nyu.edu/faculty/caitlin-j-guo', 'displayed_link': 'https://med.nyu.edu › faculty › caitlin-j-guo', 'favicon': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488c448b4b7cfebc2d26082958894c2d5e.png', 'snippet': 'Caitlin J. Guo, MD. Clinical Associate Professor, Department of Anesthesiology, Perioperative Care, and Pain Medicine. Positions & Education; Publications ...', 'snippet_highlighted_words': ['Caitlin', 'Guo'], 'about_this_result': {'keywords': ['guo'], 'related_keywords': ['caitlin'], 'languages': ['English'], 'regions': ['United States']}, 'cached_page_link': 'https://webcache.googleusercontent.com/search?q=cache:WVr47h_15KQJ:https://med.nyu.edu/faculty/caitlin-j-guo&cd=21&hl=en&ct=clnk&gl=us', 'source': 'New York University'}, {'position': 3, 'title': 'caitlyn-guo Profiles', 'link': 'https://en-gb.facebook.com/public/Caitlyn-Guo', 'displayed_link': 'https://en-gb.facebook.com › public › Caitlyn-Guo', 'favicon': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b13848d4600b6575b17c631def85a43f187689.png', 'snippet': 'View the profiles of people named Caitlyn Guo. Join Facebook to connect with Caitlyn Guo and others you may know. Facebook gives people the power to...', 'snippet_highlighted_words': ['Caitlyn Guo', 'Caitlyn Guo'], 'about_this_result': {'keywords': ['caitlyn', 'guo'], 'languages': ['English'], 'regions': ['United States']}, 'cached_page_link': 'https://webcache.googleusercontent.com/search?q=cache:Bfaz9UPTPTQJ:https://en-gb.facebook.com/public/Caitlyn-Guo&cd=22&hl=en&ct=clnk&gl=us', 'source': 'Facebook'}, {'position': 4, 'title': "Caitlyn Guo's (cbguo2) software portfolio", 'link': 'https://devpost.com/cbguo2', 'displayed_link': 'https://devpost.com › cbguo2', 'favicon': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138481948d8785276c0605ceed213a16d9fe9.png', 'snippet': 'Caitlyn Guo specializes in Java, HTML5, Google Maps, Photoshop, Adobe Illustrator, and Python. Follow Caitlyn Guo on Devpost!', 'snippet_highlighted_words': ['Caitlyn Guo', 'Caitlyn Guo'], 'about_this_result': {'keywords': ['caitlyn', 'guo'], 'languages': ['English'], 'regions': ['United States']}, 'cached_page_link': 'https://webcache.googleusercontent.com/search?q=cache:RaTRsqeRW04J:https://devpost.com/cbguo2&cd=23&hl=en&ct=clnk&gl=us', 'source': 'Devpost'}, {'position': 5, 'title': 'Caitlyn Guo (@caitlyng52) / Twitter', 'link': 'https://twitter.com/caitlyng52', 'displayed_link': 'https://twitter.com › caitlyng52', 'favicon': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b1384881ac62262921740fcd870f64ac441971.png', 'snippet': 'See new Tweets. Opens profile photo. Follow. Click to Follow caitlyng52. Caitlyn Guo. @caitlyng52. Joined October 2014.', 'snippet_highlighted_words': ['Caitlyn Guo'], 'about_this_result': {'keywords': ['caitlyn', 'guo'], 'languages': ['English'], 'regions': ['United States']}, 'cached_page_link': 'https://webcache.googleusercontent.com/search?q=cache:B7fHhYXNTQIJ:https://twitter.com/caitlyng52&cd=24&hl=en&ct=clnk&gl=us', 'source': 'Twitter'}, {'position': 6, 'title': "Caitlyn Guo's Instagram, Twitter & Facebook", 'link': 'https://www.idcrawl.com/caitlyn-guo', 'displayed_link': 'https://www.idcrawl.com › caitlyn-guo', 'thumbnail': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b1384810888a4127fe0adc572a1870efa313af.jpeg', 'favicon': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138484b3674fc1d9f6dc4ad608165fde64ca9.png', 'snippet': 'Caitlyn B Guo from Plainsboro, New Jersey. Caitlyn B Guo (age 21) is listed at 104 Tennyson Dr Plainsboro, Nj 08536 and is affiliated with the Democratic Party.', 'snippet_highlighted_words': ['Caitlyn', 'Guo', 'Caitlyn', 'Guo'], 'images': ['https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2dfb58b640be545cf0.jpeg', 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2d48114b5544f07042.jpeg', 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2ddbe200299742905b.jpeg', 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2d004d95f67efc58ba.jpeg', 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2d8c8f8c621855ce75.jpeg', 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2de5bd2288c4f14229.jpeg'], 'about_this_result': {'keywords': ['caitlyn', 'guo'], 'languages': ['English'], 'regions': ['United States']}, 'cached_page_link': 'https://webcache.googleusercontent.com/search?q=cache:O5GzeUULmR8J:https://www.idcrawl.com/caitlyn-guo&cd=25&hl=en&ct=clnk&gl=us', 'source': 'IDCrawl'}, {'position': 7, 'title': 'Caitlyn Guo cbguo2', 'link': 'https://github.com/cbguo2', 'displayed_link': 'https://github.com › cbguo2', 'thumbnail': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138482ee67ec0f3ca8841fc09e66294b6e913.jpeg', 'favicon': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b1384881ea8975da7ce372f60a1b5a1e8d78be.png', 'about_this_result': {'keywords': ['caitlyn', 'guo'], 'languages': ['English'], 'regions': ['United States']}, 'cached_page_link': 'https://webcache.googleusercontent.com/search?q=cache:cgB2_Q84zV0J:https://github.com/cbguo2&cd=26&hl=en&ct=clnk&gl=us', 'rich_snippet_table': [{'day_of_week': 'Sunday Sun', 'august_aug': 'No contributions on Sunday, Au...'}, {'day_of_week': 'Monday Mon', 'august_aug': 'No contributions on Monday, Au...'}, {'day_of_week': 'Tuesday Tue', 'august_aug': 'No contributions on Tuesday, A...'}], 'source': 'GitHub'}, {'position': 8, 'title': 'Caitlin Guo — OfficialUSA.com Records', 'link': 'https://www.officialusa.com/names/Caitlin-Guo/', 'displayed_link': 'https://www.officialusa.com › names › Caitlin-Guo', 'favicon': 'https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b13848c0fa7678e5c986968a33e6d88eb4717f.png', 'snippet': "3-11-1980 is her birth date. Caitlin's age is 42 years. Caitlin's residency is at 222 East 34th Strt, NY, NY 10016. We hold information about companies such ...", 'snippet_highlighted_words': ["Caitlin's", "Caitlin's"], 'about_this_result': {'keywords': ['guo'], 'related_keywords': ['caitlin'], 'languages': ['English'], 'regions': ['United States']}, 'cached_page_link': 'https://webcache.googleusercontent.com/search?q=cache:hautF9bwjTcJ:https://www.officialusa.com/names/Caitlin-Guo/&cd=27&hl=en&ct=clnk&gl=us', 'source': 'Official USA'}], 'pagination': {'current': 1, 'next': 'https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&start=10&sourceid=chrome&ie=UTF-8', 'other_pages': {'2': 'https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&start=10&sourceid=chrome&ie=UTF-8', '3': 'https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&start=20&sourceid=chrome&ie=UTF-8', '4': 'https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&start=30&sourceid=chrome&ie=UTF-8', '5': 'https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&start=40&sourceid=chrome&ie=UTF-8'}}, 'serpapi_pagination': {'current': 1, 'next_link': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=10', 'next': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=10', 'other_pages': {'2': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=10', '3': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=20', '4': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=30', '5': 'https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=40'}}}
'''

correct_output = '''
{
	"search_metadata": {
		"id": "64d830434055aa6183cebb38",
		"status": "Success",
		"json_endpoint": "https://serpapi.com/searches/1d4a53df43c88119/64d830434055aa6183cebb38.json",
		"created_at": "2023-08-13 01:22:11 UTC",
		"processed_at": "2023-08-13 01:22:11 UTC",
		"google_url": "https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&sourceid=chrome&ie=UTF-8",
		"raw_html_file": "https://serpapi.com/searches/1d4a53df43c88119/64d830434055aa6183cebb38.html",
		"total_time_taken": 1.89
	},
	"search_parameters": {
		"engine": "google",
		"q": "Caitlyn Guo",
		"google_domain": "google.com",
		"device": "desktop"
	},
	"search_information": {
		"organic_results_state": "Results for exact spelling",
		"query_displayed": "Caitlyn Guo",
		"total_results": 1220000,
		"time_taken_displayed": 0.3,
		"menu_items": [{
			"position": 1,
			"title": "Images",
			"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQICxAB",
			"serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google_images&gl=us&google_domain=google.com&hl=en&q=Caitlyn+Guo"
		}, {
			"position": 2,
			"title": "News",
			"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=nws&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQIChAB",
			"serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&tbm=nws"
		}, {
			"position": 3,
			"title": "Videos",
			"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=vid&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQICRAB",
			"serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google_videos&gl=us&google_domain=google.com&hl=en&q=Caitlyn+Guo"
		}, {
			"position": 4,
			"title": "Shopping",
			"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=shop&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQIDBAB",
			"serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google_shopping&gl=us&google_domain=google.com&hl=en&q=Caitlyn+Guo"
		}, {
			"position": 5,
			"title": "Books",
			"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=bks&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQIOBAB"
		}, {
			"position": 6,
			"title": "Maps",
			"link": "https://maps.google.com/maps?sca_esv=556415102&output=search&q=Caitlyn+Guo&source=lnms&entry=mc&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQIORAB"
		}, {
			"position": 7,
			"title": "Flights",
			"link": "https://www.google.com/travel/flights?sca_esv=556415102&output=search&q=Caitlyn+Guo&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQINxAB"
		}, {
			"position": 8,
			"title": "Finance",
			"link": "https://www.google.com/finance?sca_esv=556415102&output=search&q=Caitlyn+Guo&source=lnms&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ0pQJegQIOhAB"
		}]
	},
	"inline_images": [{
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgNEAA#imgrc=JZ4gPqNdLmaJmM",
		"source": "https://github.com/cbguo2",
		"thumbnail": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab63115e21c470f7e08e5b260207796138b0f41e059a2287034742.jpeg",
		"original": "https://avatars.githubusercontent.com/u/42985049?v=4",
		"title": "cbguo2 (Caitlyn Guo) · GitHub",
		"source_name": "GitHub"
	}, {
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgPEAA#imgrc=-dOn-q5vcS6AaM",
		"source": "https://www.linkedin.com/in/cguo82",
		"thumbnail": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab63116404133f2e49c28868985bbee2d6c134201a93ca159d142b.jpeg",
		"original": "https://media.licdn.com/dms/image/C4D03AQEyAf3ohwufaw/profile-displayphoto-shrink_800_800/0/1628880583050?e=2147483647&v=beta&t=AAe-VhgGx-_cpJb64t6SiHcveqzH0soLcudJTaXHvpw",
		"title": "Caitlyn Guo - Software Engineer - Uber | LinkedIn",
		"source_name": "LinkedIn"
	}, {
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgYEAA#imgrc=pogNSGyjcRi3eM",
		"source": "https://devpost.com/cbguo2",
		"thumbnail": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab6311dbd8855353284a01c266c6fddae720aab5cb69b8e6875896.jpeg",
		"original": "https://d112y698adiu2z.cloudfront.net/photos/production/user_photos/000/770/874/datas/xlarge.png",
		"title": "Caitlyn Guo's (cbguo2) software portfolio | Devpost",
		"source_name": "Devpost"
	}, {
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgSEAA#imgrc=cNlZJWpeZiwkjM",
		"source": "https://sg.linkedin.com/in/caitlyn-guo-yiyun-9a27751a8",
		"thumbnail": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab631168cab74cf1f9d8af51e1e769987ac87e27cb6c152c3d2ce5.jpeg",
		"original": "https://media.licdn.com/dms/image/D5603AQHEchx4JZBl8A/profile-displayphoto-shrink_800_800/0/1669787270885?e=2147483647&v=beta&t=RVCunExh55aVZXhGEHPrGpfwdaApzJepr5OSO-TczLg",
		"title": "Caitlyn Guo Yiyun - Global Management Trainee - Qudian(趣店 ...",
		"source_name": "LinkedIn"
	}, {
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgUEAA#imgrc=eQgD-Nth5qtGOM",
		"source": "https://www.linkedin.com/in/cguo82",
		"thumbnail": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab6311d913e9348da4099031fffe452bd353edf0f9067814e2bc1c.jpeg",
		"original": "https://media.licdn.com/dms/image/C4E22AQEakkyFLmvmIA/feedshare-shrink_800/0/1622418596388?e=2147483647&v=beta&t=J1lR2vytDrej0xGxEK_zte04z_5NuuC-budBrzD7v_0",
		"title": "Caitlyn Guo - Software Engineer - Uber | LinkedIn",
		"source_name": "LinkedIn"
	}, {
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgREAA#imgrc=NENm3o49jdNQcM",
		"source": "https://www.racked.com/2016/4/21/11477318/time-100-2016",
		"thumbnail": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab631128289d7d3217add9335215ceffe48d37cdb412a079bfad73.jpeg",
		"original": "https://cdn.vox-cdn.com/thumbor/3KK8Bdwjq8Ad-RWR8dXephgLOyc=/60x0:2932x2154/1400x1050/filters:focal(60x0:2932x2154):format(jpeg)/cdn.vox-cdn.com/uploads/chorus_image/image/49366163/GettyImages-520691680.0.0.jpg",
		"title": "Karlie Kloss, Guo Pei, and Caitlyn Jenner Make the Time 100 ...",
		"source_name": "Racked"
	}, {
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgTEAA#imgrc=6cN3gqcYj_i3oM",
		"source": "https://twitter.com/CityofLdnOnt/status/1437880121797513238",
		"thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfW3eJhoYo4lJOZREz73MtR49TrWnKfAGESFnVbsIxvw&s",
		"original": "https://pbs.twimg.com/media/E_RgWYrWEAAHuUe.jpg",
		"title": "City of London on Twitter: \"Congratulations to Cindy Sun ...",
		"source_name": "Twitter"
	}, {
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgXEAA#imgrc=5krV66uEYNn5_M",
		"source": "https://www.berkeleyubg.org/our-members",
		"thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEjuFVLtSKZrnNQE2juSWBQ4d6ymA9IhFgySi1qgYC&s",
		"original": "https://images.squarespace-cdn.com/content/v1/5ff6cf81cca0501131aedc5c/f0db8c8b-e911-4ec2-8933-7790542952d2/318248018_703932874448713_7612557329667606544_n.jpg",
		"title": "Members — Undergraduate Business Group",
		"source_name": "Undergraduate Business Group"
	}, {
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgOEAA#imgrc=H-BTKTrKqvvd-M",
		"source": "https://www.berkeleyubg.org/our-members",
		"thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBXkennsoVk-kpRnp-WJx1EJDRZ0iZn9NV1fcvc0fb&s",
		"original": "https://images.squarespace-cdn.com/content/v1/5ff6cf81cca0501131aedc5c/cac9f675-1be3-40b4-a279-cd62a8e1b921/322541198_972545480390608_2636439282626952368_n.jpg",
		"title": "Members — Undergraduate Business Group",
		"source_name": "Undergraduate Business Group"
	}, {
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&source=univ&fir=JZ4gPqNdLmaJmM%252CcgB2_Q84zV3HmM%252C_%253B-dOn-q5vcS6AaM%252CN5ZMtka-iRq1hM%252C_%253BpogNSGyjcRi3eM%252CRaTRsqeRW05pyM%252C_%253BcNlZJWpeZiwkjM%252CK46qzU2w9Lw5TM%252C_%253BeQgD-Nth5qtGOM%252CN5ZMtka-iRq1hM%252C_%253BNENm3o49jdNQcM%252C8wBqvYncI8kyqM%252C_%253B6cN3gqcYj_i3oM%252CDUiGD2d8-KYVnM%252C_%253B5krV66uEYNn5_M%252CvUsyJ583htuXgM%252C_%253BH-BTKTrKqvvd-M%252CvUsyJ583htuXgM%252C_%253Bbe0WY7RoWz-V2M%252CHlicD_oZMu5LoM%252C_&usg=AI4_-kTFJVk45h5RxEksZWQjmqZQeRTtGQ&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQ9AF6BAgQEAA#imgrc=be0WY7RoWz-V2M",
		"source": "https://ucsdtritons.com/sports/fencing/roster/caitlyn-callaghan/2713",
		"thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSL5pvTKAlh_QuPcTa7uK2q0evuGGuJ6AmGCzv_sl2z&s",
		"original": "https://ucsdtritons.com/images/2017/11/21/FSXPTIIMHUBQXYK.20171121173910.jpg?width=300",
		"title": "Caitlyn Callaghan - 2017-18 - Fencing - UC San Diego",
		"source_name": "UC San Diego Athletics"
	}],
	"inline_images_suggested_searches": [{
		"name": "queen elizabeth",
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&chips=q:caitlyn+guo,online_chips:queen+elizabeth:uf4Lr-R20qY%3D&usg=AI4_-kSpMXcn9_yLFOT5ljBATjAxOXXTAA&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQgIoDKAB6BAgZEBI",
		"chips": "q:caitlyn+guo,online_chips:queen+elizabeth:uf4Lr-R20qY%3D",
		"serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo",
		"thumbnail": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab63117c20c5e6a19e57e53482a23cbb6fcd6ffbf64653dd9005cb10ad5434c7947eaf1f1bcc944150573e.jpeg"
	}, {
		"name": "scherba",
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&chips=q:caitlyn+guo,online_chips:scherba&usg=AI4_-kRpkVtbG7W8W33H2tFR0uDVWlOGMg&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQgIoDKAF6BAgZEBY",
		"chips": "q:caitlyn+guo,online_chips:scherba",
		"serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo"
	}, {
		"name": "shilbayeh",
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&chips=q:caitlyn+guo,online_chips:shilbayeh&usg=AI4_-kT1WpeMYdPkPzVvO3wLxGci6wzKdg&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQgIoDKAJ6BAgZEBk",
		"chips": "q:caitlyn+guo,online_chips:shilbayeh",
		"serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo"
	}, {
		"name": "elizabeth scholarship",
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&chips=q:caitlyn+guo,online_chips:elizabeth+scholarship&usg=AI4_-kQys-FQ7te2alQxvYIEi7IKtbvCzA&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQgIoDKAN6BAgZEBw",
		"chips": "q:caitlyn+guo,online_chips:elizabeth+scholarship",
		"serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo"
	}, {
		"name": "software engineer",
		"link": "https://www.google.com/search?sca_esv=556415102&q=Caitlyn+Guo&tbm=isch&chips=q:caitlyn+guo,online_chips:software+engineer:LnFvrvqn0_k%3D&usg=AI4_-kQivFbTOCC12VqzDWkldvNO0EInHA&sa=X&ved=2ahUKEwikgP6zvNiAAxVGOkQIHeDCBuoQgIoDKAR6BAgZEB8",
		"chips": "q:caitlyn+guo,online_chips:software+engineer:LnFvrvqn0_k%3D",
		"serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo",
		"thumbnail": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/d842ca498dab63117c20c5e6a19e57e53482a23cbb6fcd6ffbf64653dd9005cb5fb263c26143176cb957f9612ce2bf00.jpeg"
	}],
	"organic_results": [{
		"position": 1,
		"title": "Caitlyn Guo - Software Engineer - Uber",
		"link": "https://www.linkedin.com/in/cguo82",
		"displayed_link": "https://www.linkedin.com › cguo82",
		"favicon": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b13848b6fdc706eafa2eca266e8f091ddf2795.png",
		"snippet": "View the profiles of professionals named \"Caitlyn Guo\" on LinkedIn. There are 2 professionals named \"Caitlyn Guo\", who use LinkedIn to exchange information, ...",
		"snippet_highlighted_words": ["Caitlyn Guo", "Caitlyn Guo"],
		"about_this_result": {
			"keywords": ["caitlyn", "guo"],
			"languages": ["English"],
			"regions": ["United States"]
		},
		"rich_snippet_list": ["Software Engineer at Uber", "Activity", "Experience", "Education", "Volunteer Experience", "Courses", "Projects"],
		"source": "LinkedIn",
		"related_results": [{
			"position": 1,
			"title": "2 \"Caitlyn Guo\" profiles",
			"link": "https://www.linkedin.com/pub/dir/Caitlyn/Guo",
			"displayed_link": "https://www.linkedin.com › pub › dir › Caitlyn › Guo",
			"snippet": "View the profiles of professionals named \"Caitlyn Guo\" on LinkedIn. There are 2 professionals named \"Caitlyn Guo\", who use LinkedIn to exchange information, ...",
			"snippet_highlighted_words": ["Caitlyn Guo", "Caitlyn Guo"],
			"about_this_result": {
				"keywords": ["caitlyn", "guo"],
				"languages": ["English"],
				"regions": ["United States"]
			}
		}]
	}, {
		"position": 2,
		"title": "Caitlin J. Guo, MD",
		"link": "https://med.nyu.edu/faculty/caitlin-j-guo",
		"displayed_link": "https://med.nyu.edu › faculty › caitlin-j-guo",
		"favicon": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488c448b4b7cfebc2d26082958894c2d5e.png",
		"snippet": "Caitlin J. Guo, MD. Clinical Associate Professor, Department of Anesthesiology, Perioperative Care, and Pain Medicine. Positions & Education; Publications ...",
		"snippet_highlighted_words": ["Caitlin", "Guo"],
		"about_this_result": {
			"keywords": ["guo"],
			"related_keywords": ["caitlin"],
			"languages": ["English"],
			"regions": ["United States"]
		},
		"cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:WVr47h_15KQJ:https://med.nyu.edu/faculty/caitlin-j-guo&cd=21&hl=en&ct=clnk&gl=us",
		"source": "New York University"
	}, {
		"position": 3,
		"title": "caitlyn-guo Profiles",
		"link": "https://en-gb.facebook.com/public/Caitlyn-Guo",
		"displayed_link": "https://en-gb.facebook.com › public › Caitlyn-Guo",
		"favicon": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b13848d4600b6575b17c631def85a43f187689.png",
		"snippet": "View the profiles of people named Caitlyn Guo. Join Facebook to connect with Caitlyn Guo and others you may know. Facebook gives people the power to...",
		"snippet_highlighted_words": ["Caitlyn Guo", "Caitlyn Guo"],
		"about_this_result": {
			"keywords": ["caitlyn", "guo"],
			"languages": ["English"],
			"regions": ["United States"]
		},
		"cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:Bfaz9UPTPTQJ:https://en-gb.facebook.com/public/Caitlyn-Guo&cd=22&hl=en&ct=clnk&gl=us",
		"source": "Facebook"
	}, {
		"position": 4,
		"title": "Caitlyn Guo's (cbguo2) software portfolio",
		"link": "https://devpost.com/cbguo2",
		"displayed_link": "https://devpost.com › cbguo2",
		"favicon": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138481948d8785276c0605ceed213a16d9fe9.png",
		"snippet": "Caitlyn Guo specializes in Java, HTML5, Google Maps, Photoshop, Adobe Illustrator, and Python. Follow Caitlyn Guo on Devpost!",
		"snippet_highlighted_words": ["Caitlyn Guo", "Caitlyn Guo"],
		"about_this_result": {
			"keywords": ["caitlyn", "guo"],
			"languages": ["English"],
			"regions": ["United States"]
		},
		"cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:RaTRsqeRW04J:https://devpost.com/cbguo2&cd=23&hl=en&ct=clnk&gl=us",
		"source": "Devpost"
	}, {
		"position": 5,
		"title": "Caitlyn Guo (@caitlyng52) / Twitter",
		"link": "https://twitter.com/caitlyng52",
		"displayed_link": "https://twitter.com › caitlyng52",
		"favicon": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b1384881ac62262921740fcd870f64ac441971.png",
		"snippet": "See new Tweets. Opens profile photo. Follow. Click to Follow caitlyng52. Caitlyn Guo. @caitlyng52. Joined October 2014.",
		"snippet_highlighted_words": ["Caitlyn Guo"],
		"about_this_result": {
			"keywords": ["caitlyn", "guo"],
			"languages": ["English"],
			"regions": ["United States"]
		},
		"cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:B7fHhYXNTQIJ:https://twitter.com/caitlyng52&cd=24&hl=en&ct=clnk&gl=us",
		"source": "Twitter"
	}, {
		"position": 6,
		"title": "Caitlyn Guo's Instagram, Twitter & Facebook",
		"link": "https://www.idcrawl.com/caitlyn-guo",
		"displayed_link": "https://www.idcrawl.com › caitlyn-guo",
		"thumbnail": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b1384810888a4127fe0adc572a1870efa313af.jpeg",
		"favicon": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138484b3674fc1d9f6dc4ad608165fde64ca9.png",
		"snippet": "Caitlyn B Guo from Plainsboro, New Jersey. Caitlyn B Guo (age 21) is listed at 104 Tennyson Dr Plainsboro, Nj 08536 and is affiliated with the Democratic Party.",
		"snippet_highlighted_words": ["Caitlyn", "Guo", "Caitlyn", "Guo"],
		"images": ["https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2dfb58b640be545cf0.jpeg", "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2d48114b5544f07042.jpeg", "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2ddbe200299742905b.jpeg", "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2d004d95f67efc58ba.jpeg", "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2d8c8f8c621855ce75.jpeg", "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138488fa97a976610cb2de5bd2288c4f14229.jpeg"],
		"about_this_result": {
			"keywords": ["caitlyn", "guo"],
			"languages": ["English"],
			"regions": ["United States"]
		},
		"cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:O5GzeUULmR8J:https://www.idcrawl.com/caitlyn-guo&cd=25&hl=en&ct=clnk&gl=us",
		"source": "IDCrawl"
	}, {
		"position": 7,
		"title": "Caitlyn Guo cbguo2",
		"link": "https://github.com/cbguo2",
		"displayed_link": "https://github.com › cbguo2",
		"thumbnail": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b138482ee67ec0f3ca8841fc09e66294b6e913.jpeg",
		"favicon": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b1384881ea8975da7ce372f60a1b5a1e8d78be.png",
		"about_this_result": {
			"keywords": ["caitlyn", "guo"],
			"languages": ["English"],
			"regions": ["United States"]
		},
		"cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:cgB2_Q84zV0J:https://github.com/cbguo2&cd=26&hl=en&ct=clnk&gl=us",
		"rich_snippet_table": [{
			"day_of_week": "Sunday Sun",
			"august_aug": "No contributions on Sunday, Au..."
		}, {
			"day_of_week": "Monday Mon",
			"august_aug": "No contributions on Monday, Au..."
		}, {
			"day_of_week": "Tuesday Tue",
			"august_aug": "No contributions on Tuesday, A..."
		}],
		"source": "GitHub"
	}, {
		"position": 8,
		"title": "Caitlin Guo — OfficialUSA.com Records",
		"link": "https://www.officialusa.com/names/Caitlin-Guo/",
		"displayed_link": "https://www.officialusa.com › names › Caitlin-Guo",
		"favicon": "https://serpapi.com/searches/64d830434055aa6183cebb38/images/70a13eec84c1726c9ca310db76b13848c0fa7678e5c986968a33e6d88eb4717f.png",
		"snippet": "3-11-1980 is her birth date. Caitlin's age is 42 years. Caitlin's residency is at 222 East 34th Strt, NY, NY 10016. We hold information about companies such ...",
		"snippet_highlighted_words": ["Caitlin's", "Caitlin's"],
		"about_this_result": {
			"keywords": ["guo"],
			"related_keywords": ["caitlin"],
			"languages": ["English"],
			"regions": ["United States"]
		},
		"cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:hautF9bwjTcJ:https://www.officialusa.com/names/Caitlin-Guo/&cd=27&hl=en&ct=clnk&gl=us",
		"source": "Official USA"
	}],
	"pagination": {
		"current": 1,
		"next": "https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&start=10&sourceid=chrome&ie=UTF-8",
		"other_pages": {
			"2": "https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&start=10&sourceid=chrome&ie=UTF-8",
			"3": "https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&start=20&sourceid=chrome&ie=UTF-8",
			"4": "https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&start=30&sourceid=chrome&ie=UTF-8",
			"5": "https://www.google.com/search?q=Caitlyn+Guo&oq=Caitlyn+Guo&start=40&sourceid=chrome&ie=UTF-8"
		}
	},
	"serpapi_pagination": {
		"current": 1,
		"next_link": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=10",
		"next": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=10",
		"other_pages": {
			"2": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=10",
			"3": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=20",
			"4": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=30",
			"5": "https://serpapi.com/search.json?device=desktop&engine=google&google_domain=google.com&q=Caitlyn+Guo&start=40"
		}
	}
}
'''

# Convert JSON string to a JSON data object
data = json.loads(correct_output)

print(data['organic_result'])