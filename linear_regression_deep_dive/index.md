# Linear Regression Deep Dive
---

## 22/03/26
Project started today!

## 31/03/26

I have actually been working on this, but haven't made much progress as I've
been busy with a bunch of other projects (most notably, the [Rocket
Clock](../led_streaming_display___rocket_countdown/) which is close to being
done.

One thing I will write here, though, is that I've been looking at linear
transforms, or rather, revising them again. I wanted to visualise what happens
in a 2d transform, specifically, to the basis vectors (and therefore, the entire
"space" of that 2D system). Not super important in terms of linear regression,
except that a linear system is one that:

- is additive
- is homogeneous

### Additive

Formally, this is defined as:

$$ f(x+y) = f(x)+f(y) $$

This is a fancy way of saying if you have a function, say $$ f(x) = 1 + x $$ and
you want to test if it's additive:

$$ f(3) = 1 + 3 = 4; f(1) + f(2) = 1 + 1 + 1 + 2 = 5 $$

So, this function is not linear (or at least, not additive). An example of one
would be:

$$ f(x) = 2 \cdot x $$

Interestingly, the function we mentioned ($$ f(x) = 1 + x$$) is an __affine__
transform, which we actually use in linear regression! So it's not strictly a
linear transform, rather an affine transform, but they still call it so. An
affine transform is a linear transform with some shifting origin.

## 13/04/26

Been a while since I've picked this up, so let's continue.

### Homegenity

Formally, this is written as:

$$ f(cx) = c \cdot f(x) $$

A scaled input yields a scaled output. Let's say we have the function in our
previous example, $$ f(x) = x + 1 $$.

Let's see if it's also homogenious:

$$ f(10 \cdot x) $$

This means, multiply $$x$$ by 10, then put it into our function:

$$ f(10 \cdot x) = 1 + 10 \cdot x $$

That's scaling the input. Scaling the output:

$$ c \cdot f(x) = 10 * (1 + x) = 10 + 10 \cdot x $$

Since $$ 1 + 10 \cdot x \neq 10 + 10 \cdot x $$ then this function in (again)
not linear.

### Exploring linear transformations in vectors

Linear transforms can be done quite well and compactly with vectors. A 2D matrix 
$$ A $$ can be used to detail what happens to the basis vectors of the orignal
vector, to transform it to the space of the new space. Let's first consider a 2D
"world". Often, it's easier to see said world by viewing the grid lines:

![image](./images/Grid.png)


