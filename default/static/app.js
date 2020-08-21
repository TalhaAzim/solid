const vm = new Vue({
    el: '#vm',
    data: {
        posts: []
    }
});

Vue.component('blog-post', {
    props: ['post'],
    template: `<article v-bind:id="post.id">
        <header>
            <h1>{{ post.title }}</h1>
            <span>By {{ post.author.name }} on {{ post.date_published }}</span>
        </header>
        <div v-html="post.body"></div>
        <footer>
            <ul>
                <li class="badge bg-primary text-light" v-for="tag of post.tags">{{ tag }}</li>
            </ul>
        </footer>
    </article>`
});

Vue.component('blog-roll', {
    props: ['posts'],
    template: `<ul>
        <li v-for="post of posts"><blog-post v-bind:post="post"></blog-post></li>
    </ul>`
})

fetch("https://solid-blog-simulation.uc.r.appspot.com/api/posts")
        .then(r => r.json()).then(j => vm.posts = j);