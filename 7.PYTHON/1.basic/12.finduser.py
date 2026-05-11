def find_user_and_return(name):
    found =[] #찾은 사용자를 담을 바구니 (리스틉 변수)
    for user in usere:
        if user["name"].startswith(name):