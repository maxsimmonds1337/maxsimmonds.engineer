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
