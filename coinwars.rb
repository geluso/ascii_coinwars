class Coinwars < Formula
  desc "A playable ASCII digitization of Coin Wars, a turn-based tactical strategy game pitting teams
  homepage "http://coinwars.org/ascii"
  url "https://github.com/geluso/ascii_coinwars/archive/1.0.1.tar.gz"
  sha256 "c1759b94e5f145d9dac2d022256e99618fb6316eaea2e9c43bb7cb356dfcdb01"

  depends_on "python3"

  resource "cffi" do
    url "https://files.pythonhosted.org/packages/a1/32/e3d6c3a8b5461b903651dd6ce958ed03c093d2e00128e3
    sha256 "563e0bd53fda03c151573217b3a49b3abad8813de9dd0632e10090f6190fdaf8"
  end 

  resource "pycparser" do
    url "https://files.pythonhosted.org/packages/be/64/1bb257ffb17d01f4a38d7ce686809a736837ad4371bcc5
    sha256 "0aac31e917c24cb3357f5a4d5566f2cc91a19ca41862f6c3c22dc60a629673b6"
  end 

  resource "pymunk" do
    url "https://files.pythonhosted.org/packages/07/a7/1770c435971e2178d77052e36d6f69cc27eab7f395f766
    sha256 "d8b22479c71b886b34c103ca7d272aa207a974057ba90eeb85be2e793ff36d4a"
  end 

  include Language::Python::Virtualenv

  def install
    virtualenv_install_with_resources
  end 
end
