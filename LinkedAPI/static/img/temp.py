import requests
myToken = 'AQXPg1iKkIU-wCp_HZ2p1sRxO1xz4_41A2yabzO8i7pLiggjcvZ5h9pbLlyVHWbL1Wabvoe20eSY3P5q2_76i-Vv1y-2XjMB-Q8tdFT7_JlYZndlK2LEtyJAggh_BKtVJ2y1hYXd0R0JEnMt7fJOTAuspoaONdTU_UisFDs_njsfHgeIYhbjHaa9r-lvolLQlY-s1o_EjLfT3CGzOF_ZvqYxpdlQFCEOMzh_EKrMPatgP6_G1R4QdOxkRtw1_kj6Xy44yuB7ZpjfCXZS7I6dwxr7ILDubq5lexcMh16Mt07gakSUaVErMU4XmSbOGU2MCibOrrqq8b1lNNaKhLdK73OWcQ_t9g'
myUrl = 'https://api.linkedin.com/v2/me'
head = {'Authorization': 'Bearer {}'.format(myToken)}
response = requests.get(myUrl, headers=head)
print(response.json())