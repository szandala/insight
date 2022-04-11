export default function AuthHeader() {
  const user = JSON.parse(localStorage.getItem("user"));

  if (user && user.token) {
    return { 'x-access-token': user.token };       // for Flask / Node.js Express back-end
       // return { Authorization: "Bearer " + user.token }; // for other
  } else {
    return {};
  }
}
