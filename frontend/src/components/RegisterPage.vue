<template>
     <div>
        <div class="page-body">
            <form class="card">
                <div class="card-header">
                    Register
                </div>
                <div class="card-body">
                    <div class="form-group">
                        <label for="email">Email</label><br>
                        <input class="form-control" type="text" id="email"/>
                    </div>
                    <div class="form-group">
                        <label for="user">Account Name</label><br>
                        <input class="form-control" type="text" id="user"/>
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label><br>
                        <input class="form-control" type="password" id="password"/>
                    </div>
                    <div class="form-group">
                        <label for="repeatPassword">Repeat Password</label><br>
                        <input class="form-control" type="password" id="repeatPassword"/>
                    </div>
                    <button type="submit" class="btn btn-primary">Register</button>
                </div>
            </form>
        </div>
    </div>
</template>