import Vue from 'vue'
import {
  Button, Form, FormItem, Input, Message, Container,
  Header, Aside, Main, Menu, Submenu, MenuItemGroup, MenuItem,
  Breadcrumb, BreadcrumbItem, Card, Select, Option, Row, Col,
  Table, TableColumn, Switch, Tooltip, Pagination, Dialog,
  RadioGroup, Radio, RadioButton, MessageBox, Tag
} from 'element-ui'

// require styles 引入样式
// import 'quill/dist/quill.core.css'
// import 'quill/dist/quill.snow.css'
// import 'quill/dist/quill.bubble.css'

Vue.use(Button)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItemGroup)
Vue.use(MenuItem)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Card)
Vue.use(Select)
Vue.use(Option)
Vue.use(Row)
Vue.use(Col)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Switch)
Vue.use(Tooltip)
Vue.use(Pagination)
Vue.use(Dialog)
Vue.use(RadioGroup)
Vue.use(Radio)
Vue.use(RadioButton)
Vue.use(Tag)


Vue.prototype.$message = Message
Vue.prototype.$confirm = MessageBox.confirm
// Vue.use(VueQuillEditor)
