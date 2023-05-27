from flask import Flask, render_template, request, redirect, url_for
from user import User
from product import Product

# 웹 서버 시작
# build web server
APP = Flask(__name__)

# 템플릿을 렌더할 때 공통적으로 거치는 인터페이스
# when render som templates always visit this interface 
template = {
    'user': None,                   # 현재 로그인된 유저
    'user_list': User.user_list,    # 가입된 전체 유저 리스트
    'product_list': [],             # 페이지네이션 번호를 통해 물품을 보여줄 리스트(10개 제한)
    'current_page': 0,              # 페이지네이션 번호
    'user_id_list': {},
    'all_Products': Product.product_list, # 등록된 전체 물품 리스트
}

#init data -> 매번 회원가입하기 매우 귀찮기 때문에 미리 초기화 해두기!
User.add_user('abc', '123')
User.add_user('JIG', '0000')
User.add_user('KHJ', '0001')
User.add_user('NITHU', '0002')

Product.add_product(100, 100, 'MARKET')

bank_money = 100000000

#main page
@APP.route("/")
def index():
    return render_template('home.html', template=template)


##########################################################################################################
# please do not touch anything

#sign in
@APP.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['ID']
        password = request.form['PW']
        template['user'] = User.login(name, password)
        template['user_id_list']=User.user_ID_list
        if template['user'] is None:
            #fail sign in
            print('login fail')
            return render_template('login.html', template=template)
        else:
            #success sign in
            print('login success')
            return redirect('/');
    #sign in form
    return render_template('login.html', template=template)

#sign out
@APP.route('/logout')
def logout():
    User.logout()
    template['user'] = None
    return redirect('/')

#sign up
@APP.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        name = request.form['ID']
        password = request.form['PW']

        if User.add_user(name, password) == False:
            #fail signup
            print('sign up failed!')
            return redirect('')
        else:
            #success signup
            print(User.user_list)
            return render_template('home.html', template=template)
    else:
        #signup form
        return render_template('register.html', template=template)

# please do not touch anything
##########################################################################################################
# fakebank we need to build

@APP.route('/fakebank', methods=["GET", "POST"])
def fakebank():
    global bank_money
    
    if request.method == 'POST':
        amount = request.form['amount']

        if bank_money >= int(amount):
            User.add_money(amount)
            bank_money = bank_money-amount
            
        else:
            print('not enough money')
            return redirect('/');
    
    return render_template('fakebank.html', bank_money=bank_money, template=template)


##########################################################################################################
# we should build product-## lines

# product-list
@APP.route('/product')
def product():
    start, end = template['current_page']*10, template['current_page']*10+10
    template['product_list'] = Product.product_list[start:end]
    return render_template('product.html', template=template)


#product-upload
# @APP.route("/product-form", methods=["GET", "POST"])
# def Upload():
#     if request.method == 'POST':
#         Coin=request.form['coin']
#         Price=request.form['price']
#     else:
#         return redirect('/')
#     id = Product.add_product(Coin, Price, template['user'].coin)
#     template['all_Products']=Product.product_list
#     return redirect(f'/product-info/{id}')

# @APP.route('/search')
# def Search():
#     coin = request.args.get('coin')
#     template['product_list']=[]
#     for i in template['all_Products']:
#         if i.coin==coin:
#             template['product_list'].append(i)
#     return render_template('product.html', template=template)

#product-info
@APP.route('/product-info/<int:product_id>')
def product_info(product_id):
    product = Product.search(product_id)
    return render_template('product_info.html', template=template, product=product);

# product-info-update
@APP.route('/product-update/<int:product_id>', methods=["GET","POST"])
def product_update(product_id):
    product = Product.search(product_id)
    print(product ,"update...")

    product.coin=request.form['coin']
    product.price=request.form['price']

    template['all_Products'] = Product.product_list;
    print(product, '...updated')
    return redirect(f'/product-info/{product_id}')


#product-buy
@APP.route('/product-buy/<int:product_id>')
def product_buy(product_id):
    Product.buy(product_id);

    template['all_Products'] = Product.product_list
    return redirect('/product');

#product-delete
@APP.route('/product-delete/<int:product_id>')
def product_delete(product_id):
    Product.delete(product_id);

    template['all_Products'] = Product.product_list
    return redirect('/product');

# we should build product-## lines
##########################################################################################################


#pagenation
@APP.route('/page_up')
def pageUp():
    if template['current_page'] < len(Product.product_list)/10 - 1:
        template['current_page'] += 1
    return redirect('/product')

@APP.route('/page_down')
def pageDown():
    if template['current_page']*10 > 1:
        template['current_page'] -= 1
    return redirect('/product')

#실행코드
if __name__ == "__main__":
    APP.run(debug=True)
