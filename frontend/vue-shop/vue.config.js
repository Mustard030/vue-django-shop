
module.exports = {
    
 
    // 将构建好的文件输出到哪里
    outputDir: 'dist',
 
    // 是否在保存的时候使用 `eslint-loader` 进行检查。
    // 有效的值：`ture` | `false` | `"error"`
    // 当设置为 `"error"` 时，检查出的错误会触发编译失败。
    lintOnSave: true,
 
    // 使用带有浏览器内编译器的完整构建版本
    // 查阅 https://cn.vuejs.org/v2/guide/installation.html#运行时-编译器-vs-只包含运行时
   // compiler: false,
    runtimeCompiler: true, //关键点在这
    // 调整内部的 webpack 配置。
    // 查阅 https://github.com/vuejs/vue-doc-zh-cn/vue-cli/webpack.md
    chainWebpack: () => {},
    configureWebpack: () => {},
 
    // vue-loader 选项
    // 查阅 https://vue-loader.vuejs.org/zh-cn/options.html
   // vueLoader: {},
 
    // 是否为生产环境构建生成 source map？
    productionSourceMap: true,
 
    
    // 在生产环境下为 Babel 和 TypeScript 使用 `thread-loader`
    // 在多核机器下会默认开启。
    parallel: require('os').cpus().length > 1,
 
    // 是否使用 `autoDLLPlugin` 分割供应的包？
    // 也可以是一个在 DLL 包中引入的依赖的显性的数组。
    // 查阅 https://github.com/vuejs/vue-doc-zh-cn/vue-cli/cli-service.md#dll-模式
   // dll: false,
 
    // PWA 插件的选项。
    // 查阅 https://github.com/vuejs/vue-doc-zh-cn/vue-cli-plugin-pwa/README.md
    pwa: {},
 
    // 配置 webpack-dev-server 行为。
    devServer: {
        open: false,
        host: '0.0.0.0',
        port: 8080,
        https: false,
        hotOnly: false,
        // 查阅 https://github.com/vuejs/vue-doc-zh-cn/vue-cli/cli-service.md#配置代理
        proxy: 'http://localhost:80',
        before: app => {
            // `app` 是一个 express 实例
        }
    },
 
    // 三方插件的选项
    pluginOptions: {
        // ...
    }
}