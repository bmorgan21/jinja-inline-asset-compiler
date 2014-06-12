Jinja Inline Asset Compiler

{% compile %}
<style type="text/less">
.foo.bar {
  strong {
    font-size:10px;
  }
}
</style>

<style type="text/less">
h1 {
  color:red;
}
</style>

<script type='text/coffeescript'>
hello = () ->
    console.log('hello')

goodbye = () ->
    console.log('goodbye')

hello()
</script>

<script type='text/javascript'>
function voo() {
    console.log('voo');
    alert('hello2');
}
</script>

{% endcompile %}
